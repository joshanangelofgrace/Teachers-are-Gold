//
//  Teachers-are-Gold-Environment.h
//  Teachers-are-Gold
//
//  Created by Joshua Campbell on 5/3/15
//  Copyright (c) 2014 Glorious Technologies. All rights reserved.
//

// Defines about installed Pods
#import "Pods-Environment.h"

#define HAS_POD(podname) defined(COCOAPODS_POD_AVAILABLE_ ## podname)


// Unfortunately, you can't define preprocessor macros per scheme, so we're stuck
// doing it via configurations. These macros wrap that up nicely.
#define IS_DEBUG_CONFIGURATION(target)   defined(  CONFIGURATION_DEBUG_ ## target)
#define IS_TEST_CONFIGURATION(target)    defined(   CONFIGURATION_TEST_ ## target)
#define IS_ADHOC_CONFIGURATION(target)   defined(  CONFIGURATION_ADHOC_ ## target)
#define IS_PROFILE_CONFIGURATION(target) defined(CONFIGURATION_PROFILE_ ## target)
#define IS_DISTRIBUTION_CONFIGURATION()  defined(CONFIGURATION_DISTRIBUTION)

#define IS_DEBUG_BUILD   (  IS_DEBUG_CONFIGURATION(STAGING) ||   IS_DEBUG_CONFIGURATION(PRODUCTION))
#define IS_TEST_BUILD    (   IS_TEST_CONFIGURATION(STAGING) ||    IS_TEST_CONFIGURATION(PRODUCTION))
#define IS_ADHOC_BUILD   (  IS_ADHOC_CONFIGURATION(STAGING) ||   IS_ADHOC_CONFIGURATION(PRODUCTION))
#define IS_PROFILE_BUILD (IS_PROFILE_CONFIGURATION(STAGING) || IS_PROFILE_CONFIGURATION(PRODUCTION))
#define IS_DISTRIBUTION_BUILD IS_DISTRIBUTION_CONFIGURATION()

#if IS_DEBUG_CONFIGURATION(STAGING) || IS_TEST_CONFIGURATION(STAGING) || IS_ADHOC_CONFIGURATION(STAGING) || IS_PROFILE_CONFIGURATION(STAGING)
#define TARGETING_STAGING
#define IF_STAGING(stagingValue, productionValue) stagingValue
#else
#define TARGETING_PRODUCTION
#define IF_STAGING(stagingValue, productionValue) productionValue
#endif