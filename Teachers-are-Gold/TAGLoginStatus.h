//
//  TAGLoginStatus.h
//  Teachers are Gold!
//
//  Created by Joshua Campbell on 25/03/15.
//  Copyright (c) 2015 Teachers are Gold. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface TAGLoginStatus : NSObject{
    bool signedIn;
}

@property (nonatomic) bool isSignedIn;
+ (id)sharedManager;
@end
