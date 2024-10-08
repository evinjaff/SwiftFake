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

+ (void) runFFmpegCommand:(NSString *)command {
    
    
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

+ (void) getFFmpegVersion {
    NSLog(@"Checking -version");
    FFmpegSession *session = [FFmpegKit execute:@"-version"];
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


+ (void) transcodeToPCM161eWithInput: (NSString *)inputPath output:(NSString*)outputPath {
// original ffmpeg command from AntiFake https://github.com/WUSTL-CSPL/AntiFake?tab=readme-ov-file
// ffmpeg -i <source_audio_path> -acodec pcm_s16le -ac 1 -ar 16000 -ab 256k output_audio.wav
    
    NSLog(@"Checking -version");
    
    NSString *command = [NSString stringWithFormat:@"-i %@ -acodec pcm_s16le -ac 1 -ar 16000 -ab 256k %@", inputPath, outputPath];
    
    NSLog(@"%@", command);
    
    FFmpegSession *session = [FFmpegKit execute:command];
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


@end



