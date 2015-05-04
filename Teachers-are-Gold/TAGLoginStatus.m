//
//  TAGLoginStatus.m
//  Teachers are Gold!
//
//  Created by Joshua Campbell on 25/03/15.
//  Copyright (c) 2015 Teachers are Gold. All rights reserved.
//

#import "TAGLoginStatus.h"

@implementation TAGLoginStatus
@synthesize isSignedIn;

#pragma mark - Singleton Methods
+ (id)sharedManager {
    static TAGLoginStatus *sharedMyManager = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedMyManager = [[self alloc]init];
    });
    return sharedMyManager;
}

- (id)init {
    if (self = [super init]) {
        isSignedIn = NO;
    }
    return self;
}

@end
