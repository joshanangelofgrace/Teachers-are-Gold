//
//  main.m
//  Teachers-are-Gold
//
//  Created by Joshua Campbell on 5/3/15
//  Copyright (c) 2014 Glorious Technologies. All rights reserved.
//

#if HAS_POD(PixateFreestyle)
#import <PixateFreestyle/PixateFreestyle.h>
#endif

#import <UIKit/UIKit.h>
#import "TAGAppDelegate.h"

int main(int argc, char * argv[])
{
    @autoreleasepool {
        #if HAS_POD(PixateFreestyle)
        [PixateFreestyle initializePixateFreestyle];
        #endif

        return UIApplicationMain(argc, argv, nil, NSStringFromClass([TAGAppDelegate class]));
    }
}
