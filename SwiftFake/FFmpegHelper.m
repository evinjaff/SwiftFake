//
//  FFmpegHelper.m
//  SwiftFake
//
//  Created by Evin Jaff on 10/7/24.
//



#import <Foundation/Foundation.h>
#import <ffmpegkit/FFmpegKit.h>

@interface FFmpegWrapper : NSObject
+ (void)runFFmpegCommand:(NSString *)command;
@end

@implementation FFmpegWrapper

- (void)runFFmpegCommand:(NSString *)command {
    
    
    FFmpegSession *session = [FFmpegKit execute:@"-i file1.mp4 -c:v mpeg4 file2.mp4"];
    ReturnCode *returnCode = [session getReturnCode];
    if ([ReturnCode isSuccess:returnCode]) {

        // SUCCESS

    } else if ([ReturnCode isCancel:returnCode]) {

        // CANCEL

    } else {

        // FAILURE
        NSLog(@"Command failed with state %@ and rc %@.%@", [FFmpegKitConfig sessionStateToString:[session getState]], returnCode, [session getFailStackTrace]);

    }
    
}

+ (void)runFFmpegCommand:(NSString *)command {
    
    printf("Test command");
    NSLog(@"ran it");
}

@end



