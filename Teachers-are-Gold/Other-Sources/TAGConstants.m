//
//  TAGConstants.m
//  Teachers-are-Gold
//
//  Created by Joshua Campbell on 5/3/15
//  Copyright (c) 2014 Glorious Technologies. All rights reserved.
//

#import "Teachers-are-Gold-Environment.h"

// Use this file to define the values of the variables declared in the header.
// For data types that aren't compile-time constants (e.g. NSURL), use the
// TAGConstantsInitializer function below.

// See Teachers-are-Gold-Environment.h for macros that are likely applicable in
// this file. TARGETING_{STAGING,PRODUCTION} and IF_STAGING are probably
// the most useful.

// The values here are just examples.

#ifdef TARGETING_STAGING

//NSString * const TAGAPIKey = @"StagingKey";

#else

//NSString * const TAGAPIKey = @"ProductionKey";

#endif


//NSURL *TAGAPIRoot;
void __attribute__((constructor)) TAGConstantsInitializer() {
//    TAGAPIRoot = [NSURL URLWithString:IF_STAGING(@"http://myapp.com/api/staging", @"http://myapp.com/api")];
}