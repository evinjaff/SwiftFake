//
//  ConverterViewModel.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/3/24.
//

import Foundation




@Observable
class ConverterViewModel {
    
    
    
    
    
    func convertM4AToPCM(src: URL, dst: URL) -> Void {
        // Should convert the URL of an M4A file into a new URL of a file that's encoded
        
        // ffmpeg command to replicate: ffmpeg -i <source_audio_path> -acodec pcm_s16le -ac 1 -ar 16000 -ab 256k output_audio.wav
        
    }
    
    public func testFFmpegLibavformat() {
        if let version = String(validatingUTF8: av_version_info()) {
            print("FFmpeg version: \(version)")
        } else {
            print("Failed to get FFmpeg version")
        }
    }
    
    
}
