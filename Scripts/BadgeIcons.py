#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# This script reads the Info.plist in CODESIGNING_FOLDER_PATH, as well as several other
# environmental variables, and (if appropriate) badges the app's icons to indicate
# whether it targets staging or production and its version and build number.

# This is not run under continuous integration or for app store builds.
# Version and build information is hidden on very small icons, like those used
# in Spotlight.

from __future__ import print_function, unicode_literals
import AmaroLib as lib
import os.path
import itertools
from math import ceil
from sys import exit
import Foundation
import AppKit
import Quartz
import CoreText

# Bail if we're in CI or making an app store build
if lib.inContinuousIntegration or lib.isDistributionConfiguration:
    print('Not badging icons; this is a build for the App Store')
    exit(0)


FONT_NAME = 'Helvetica-Bold'


def getIconAndBaseColor(isStaging):
    if isStaging:
        baseColor = Foundation.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.168, 0.306, 0.184, 1)
        iconCharacter = '🅢'
    else:
        baseColor = Foundation.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.315, 0.108, 0.093, 1)
        iconCharacter = '🅟'

    return (iconCharacter, baseColor)


def makeAttributedVersionString(versionText, fontSize, color):
    versionParagraphStyle = AppKit.NSParagraphStyle.defaultParagraphStyle().mutableCopy()
    versionParagraphStyle.setLineBreakMode_(AppKit.NSLineBreakByClipping)
    versionParagraphStyle.setAlignment_(AppKit.NSRightTextAlignment)

    versionFont = Foundation.NSFont.fontWithName_size_(FONT_NAME, fontSize)

    versionAttributes = {
        AppKit.NSFontAttributeName: versionFont,
        AppKit.NSForegroundColorAttributeName: color,
        AppKit.NSParagraphStyleAttributeName: versionParagraphStyle
    }

    return Foundation.NSAttributedString.alloc().initWithString_attributes_(versionText, versionAttributes)


def makeAttributedIconString(iconGlyph, fontSize, color):
    iconFont = Foundation.NSFont.fontWithName_size_(FONT_NAME, fontSize)
    iconAttributes = {
        AppKit.NSFontAttributeName: iconFont,
        AppKit.NSForegroundColorAttributeName: color
    }

    return Foundation.NSAttributedString.alloc().initWithString_attributes_(iconGlyph, iconAttributes)


def getBadgeImage(approxIconHeight, staging, versionText):
    iconGlyph, baseColor = getIconAndBaseColor(staging)

    BORDER_THICKNESS = 0.25  # As a percentage of the icon diameter
    MIN_ICON_HEIGHT_FOR_VERSION_TEXT = 15  # below this, the version text will be left out

    # First, calculate the size of the version text
    versionString = makeAttributedVersionString(versionText, approxIconHeight / 2.5, Foundation.NSColor.whiteColor())
    versionStringBounds = versionString.boundingRectWithSize_options_(Foundation.NSZeroSize, AppKit.NSStringDrawingUsesLineFragmentOrigin)
    versionStringWidth = Foundation.NSWidth(versionStringBounds)
    if approxIconHeight < MIN_ICON_HEIGHT_FOR_VERSION_TEXT:
        versionStringWidth = 0

    # And now the icon...
    iconString = makeAttributedIconString(iconGlyph, approxIconHeight, baseColor)
    iconImage = getImageOfGlyph(iconString, Foundation.NSColor.colorWithWhite_alpha_(1.0, 0.8))
    iconSize = iconImage.size()

    # Calculate some frames and whatnot
    totalBorderThickness = Foundation.NSMakeSize(ceil(iconSize.width * BORDER_THICKNESS),
                                                 ceil(iconSize.height * BORDER_THICKNESS))

    iconOrigin = Foundation.NSMakePoint(ceil(totalBorderThickness.width / 2.0),
                                        ceil(totalBorderThickness.height / 2.0))

    borderedIconSize = Foundation.NSMakeSize(iconSize.width + totalBorderThickness.width,
                                             iconSize.height + totalBorderThickness.height)

    farRightPadding = totalBorderThickness.width / 2.0
    if versionStringWidth == 0:
        farRightPadding = 0

    badgeSize = Foundation.NSMakeSize(ceil(borderedIconSize.width + versionStringWidth + farRightPadding),
                                      borderedIconSize.height)

    rightBackgroundBoxBounds = Foundation.NSIntegralRect(
                                Foundation.NSMakeRect(borderedIconSize.width / 2.0,
                                                      0,
                                                      badgeSize.width - borderedIconSize.width / 2.0,
                                                      badgeSize.height))

    textFrameBounds = Foundation.NSIntegralRect(
                        Foundation.NSMakeRect(borderedIconSize.width,
                                              (badgeSize.height - Foundation.NSHeight(versionStringBounds)) / 2.0,  # vertically centered
                                              versionStringWidth,
                                              badgeSize.height))

    # And now drawing
    badgeImage = Foundation.NSImage.alloc().initWithSize_(badgeSize)
    badgeImage.lockFocusFlipped_(True)

    # The background rectangle + circle
    boxColor = Foundation.NSColor.colorWithCalibratedHue_saturation_brightness_alpha_(baseColor.hueComponent(), baseColor.saturationComponent(), 0.6, 1.0)
    boxColor.set()
    AppKit.NSRectFill(rightBackgroundBoxBounds)

    iconBackgroundCircleRect = (Foundation.NSZeroPoint, borderedIconSize)
    iconBackgroundCirclePath = AppKit.NSBezierPath.bezierPathWithOvalInRect_(iconBackgroundCircleRect)
    boxColor.set()
    iconBackgroundCirclePath.fill()

    # Text
    if approxIconHeight >= MIN_ICON_HEIGHT_FOR_VERSION_TEXT:
        versionString.drawInRect_(textFrameBounds)

    # The icon & its shadow
    boxShadowColor = Foundation.NSColor.colorWithWhite_alpha_(1.0, 0.7)
    boxShadow = AppKit.NSShadow.alloc().init()
    boxShadow.setShadowColor_(boxShadowColor)
    boxShadow.setShadowOffset_(Foundation.NSZeroSize)
    boxShadow.setShadowBlurRadius_(totalBorderThickness.width)
    boxShadow.set()
    
    iconDestRect = (iconOrigin, iconSize)
    iconImage.drawInRect_fromRect_operation_fraction_respectFlipped_hints_(iconDestRect, Foundation.NSZeroRect, AppKit.NSCompositeSourceAtop, 1.0, True, None)

    badgeImage.unlockFocus()

    return badgeImage


def getImageOfGlyph(glyphAttributedString, backingColor):
    line = CoreText.CTLineCreateWithAttributedString(glyphAttributedString)

    # Get a rough size of our glyph. We'll use this to make the NSImage, and get a more accurate
    # frame once we have a context to call CTLineGetImageBounds.
    typographicWidth, ascent, descent, leading = CoreText.CTLineGetTypographicBounds(line, None, None, None)

    img = Foundation.NSImage.alloc().initWithSize_(Foundation.NSMakeSize(ceil(typographicWidth), ceil(ascent + descent)))

    
    img.lockFocus()

    context = AppKit.NSGraphicsContext.currentContext().graphicsPort()

    bounds = CoreText.CTLineGetImageBounds(line, context)

    Quartz.CGContextTranslateCTM(context, 0, ceil(descent))  # Shift everything up so the descender is inside our image

    if backingColor:
        # Draw a circle behind the glyph with the ratio to the size of the glyph
        bgCircleDiameterRatio = 0.9
        bgCircleOffsetRatio = (1.0 - bgCircleDiameterRatio) / 2.0

        bgCircleRect = Foundation.NSMakeRect(bounds.origin.x + bounds.size.width * bgCircleOffsetRatio,
                                             bounds.origin.y + bounds.size.height * bgCircleOffsetRatio,
                                             bounds.size.width * bgCircleDiameterRatio,
                                            bounds.size.height * bgCircleDiameterRatio)

        backgroundCirclePath = Foundation.NSBezierPath.bezierPathWithOvalInRect_(bgCircleRect)
        backingColor.setFill()
        backgroundCirclePath.fill()

    CoreText.CTLineDraw(line, context)

    bitmapRep = Foundation.NSBitmapImageRep.alloc().initWithFocusedViewRect_(Foundation.NSIntegralRect(bounds))

    img.unlockFocus()

    finalImage = Foundation.NSImage.alloc().initWithSize_(Foundation.NSIntegralRect(bounds).size)
    finalImage.addRepresentation_(bitmapRep)

    return finalImage


def badgeFile(fn, destinationDir, isStaging, versionString, buildString):
    fullVersionString = ''
    if versionString:
        fullVersionString += 'v' + versionString
    if buildString:
        if versionString: fullVersionString += '\n'
        fullVersionString += 'b' + buildString

    # Not using -[NSImage initWithContentsOfFile:] here, since that treats @2x files
    # specially, which we don't want in this case.
    imgData = Foundation.NSData.dataWithContentsOfFile_(fn)
    img = Foundation.NSImage.alloc().initWithData_(imgData)
    size = img.size()

    # Generate the badge image
    iconHeight = size.height * 0.3
    badgeImage = getBadgeImage(iconHeight, isStaging, fullVersionString)
    badgeSize = badgeImage.size()

    # Draw it over top
    img.lockFocus()

    badgeBottomPadding = ceil(0.15 * size.height)
    badgeDestRect = ((size.width - badgeSize.width,
                      badgeBottomPadding),
                     badgeSize)
    badgeImage.drawInRect_fromRect_operation_fraction_respectFlipped_hints_(badgeDestRect, Foundation.NSZeroRect, AppKit.NSCompositeSourceAtop, 1.0, True, None)

    bitmapRep = Foundation.NSBitmapImageRep.alloc().initWithFocusedViewRect_((Foundation.NSZeroPoint, size))

    img.unlockFocus()

    # And spit the thing out
    pngData = bitmapRep.representationUsingType_properties_(AppKit.NSPNGFileType, None)

    destFn = Foundation.NSString.lastPathComponent(fn).stringByDeletingPathExtension() + '.png'
    dest = Foundation.NSString.pathWithComponents_([ destinationDir, destFn ])

    pngData.writeToFile_atomically_(dest, False)


def getIconFilenames(dir):
    # We want the processed Info.plist in the .app, not the one in the project.
    # Xcode consolidates asset catalog info into that plist, so it's a reliable
    # source for the names of icon files, regardless of how they got to be that way.
    packagedInfoPlist, _ = lib.loadPlist(os.path.join(dir, 'Info.plist'))
    iPhoneIcons = packagedInfoPlist.valueForKeyPath_('CFBundleIcons.CFBundlePrimaryIcon.CFBundleIconFiles') or []
    iPadIcons = packagedInfoPlist.valueForKeyPath_('CFBundleIcons~ipad.CFBundlePrimaryIcon.CFBundleIconFiles') or []

    allIconNames = set(itertools.chain(iPhoneIcons, iPadIcons))

    resSuffixes = ['', '@2x', '@3x']
    devSuffixes = ['', '~ipad']

    fns = [os.path.join(dir, fn + res + dev + '.png')
            for fn in allIconNames
            for res in resSuffixes
            for dev in devSuffixes]

    return filter(os.path.exists, fns)


if __name__ == '__main__':
    sourceDir = lib.getEnv('CODESIGNING_FOLDER_PATH')

    iconFns = getIconFilenames(sourceDir)

    for fn in iconFns:
        badgeFile(fn, sourceDir, lib.targetingStaging, lib.version, lib.buildNumber)

    print('Badged the following icon files: ' + ', '.join([os.path.basename(fn) for fn in iconFns]))
