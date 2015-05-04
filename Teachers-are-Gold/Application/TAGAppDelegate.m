//
//  TAGAppDelegate.m
//  Teachers-are-Gold
//
//  Created by Joshua Campbell on 5/3/15
//  Copyright (c) 2014 Glorious Technologies. All rights reserved.
//

#import "TAGAppDelegate.h"

#if HAS_POD(CocoaLumberjack)
    #if COCOAPODS_VERSION_MAJOR_CocoaLumberjack == 1
    #import <CocoaLumberjack/DDASLLogger.h>
    #import <CocoaLumberjack/DDTTYLogger.h>
    #endif

    #if HAS_POD(CrashlyticsLumberjack)
    #import <CrashlyticsLumberjack/CrashlyticsLogger.h>
    #endif

    #if HAS_POD(Sidecar)
    #import <Sidecar/CRLMethodLogFormatter.h>
    #endif
#endif

#if HAS_POD(Aperitif) && IS_ADHOC_BUILD
#import <Aperitif/CRLAperitif.h>
#endif


@implementation TAGAppDelegate

-(BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions
{
    [self initializeLoggingAndServices];
    [self setUpRemoteNotifications:application];
    
    return YES;
}

-(void)applicationDidBecomeActive:(UIApplication *)application
{
    [self scheduleCheckForUpdates];
}

/**
 *  Registers the application for remote notifications and as Parse is used to support this service, sets up any Parse integration neccessary.
 *
 *  @return nil
 */
#pragma mark Remote Notifications
- (void)setUpRemoteNotifications:(UIApplication *)application
{
    // Register for Push Notitications
    UIUserNotificationType userNotificationTypes = (UIUserNotificationTypeAlert |
                                                    UIUserNotificationTypeBadge |
                                                    UIUserNotificationTypeSound);
    UIUserNotificationSettings *settings = [UIUserNotificationSettings settingsForTypes:userNotificationTypes
                                                                             categories:nil];
    [application registerUserNotificationSettings:settings];
    [application registerForRemoteNotifications];
    
    
}

- (void)application:(UIApplication *)application didFailToRegisterForRemoteNotificationsWithError:(NSError *)error
{
    
}

- (void)application:(UIApplication *)application didReceiveLocalNotification:(UILocalNotification *)notification
{
    
}

- (void)application:(UIApplication *)application didReceiveRemoteNotification:(NSDictionary *)userInfo fetchCompletionHandler:(void (^)(UIBackgroundFetchResult))completionHandler
{
    
}

- (void)application:(UIApplication *)application didRegisterUserNotificationSettings:(UIUserNotificationSettings *)notificationSettings
{
    
}

#pragma mark General Application Management
- (void)applicationWillEnterForeground:(UIApplication *)application
{
    
}

- (void)applicationWillTerminate:(UIApplication *)application
{
    
}

#pragma mark Amaro foundation goodies

/**
 Connects to Crashlytics and sets up CocoaLumberjack
 */
-(void)initializeLoggingAndServices
{
    [Fabric with:@[CrashlyticsKit]];
    
    #if HAS_POD(CocoaLumberjack)
        #if HAS_POD(Sidecar)
        CRLMethodLogFormatter *logFormatter = [[CRLMethodLogFormatter alloc] init];
        [[DDASLLogger sharedInstance] setLogFormatter:logFormatter];
        [[DDTTYLogger sharedInstance] setLogFormatter:logFormatter];
        #endif

        // Emulate NSLog behavior for DDLog*
        [DDLog addLogger:[DDASLLogger sharedInstance]];
        [DDLog addLogger:[DDTTYLogger sharedInstance]];

        // Send warning & error messages to Crashlytics
        #if HAS_POD(CrashlyticsLumberjack)
            #if HAS_POD(Sidecar)
            [[CrashlyticsLogger sharedInstance] setLogFormatter:logFormatter];
            #endif

            [DDLog addLogger:[CrashlyticsLogger sharedInstance] withLogLevel:LOG_LEVEL_INFO];
       #endif
    #endif
}

/**
 Schedules a check for updates to the app in the Installr API. Only executed for Ad Hoc builds,
 not targetting the simulator (i.e. archives of the -Staging and -Production schemes).
 */
-(void)scheduleCheckForUpdates
{
    // Uncomment the blob below and fill in your Installr app tokens to enable automatically
    // prompting the user when a new build of your app is pushed.

    #if HAS_POD(Aperitif) && IS_ADHOC_BUILD && !TARGET_IPHONE_SIMULATOR && !defined(DEBUG)

//    #ifdef TARGETING_STAGING
//    NSString * const installrAppToken = @"<Installr app token for the staging build of your app>";
//    #else
//    NSString * const installrAppToken = @"<Installr app token for the production build of your app>";
//    #endif
//
//    [CRLAperitif sharedInstance].appToken = installrAppToken;
//    [[CRLAperitif sharedInstance] checkAfterDelay:3.0];

    #endif
}

@end
