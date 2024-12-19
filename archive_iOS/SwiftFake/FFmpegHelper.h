//
//  FFmpegHelper.h
//  SwiftFake
//
//  Created by Evin Jaff on 10/8/24.
//

#ifndef FFmpegHelper_h
#define FFmpegHelper_h


#endif /* FFmpegHelper_h */

// FFmpegWrapper.h
#import <Foundation/Foundation.h>

@interface FFmpegWrapper : NSObject

+ (void)runFFmpegCommand:(NSString *)command;
+ (void) getFFmpegVersion;
//+ (void) transcodeToPCMs161e:(NSString*)inputAudioFile;
+ (void) transcodeToPCM161eWithInput: (NSString *)inputPath output:(NSString*)outputPath;

@end
