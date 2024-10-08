//
//  ConverterViewModel.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/3/24.
//

import Foundation





@Observable
class ConverterViewModel {
    
    
    
    
    
    
    func fetchFFmpegVersion() {
//        self.ffmpegVersion = FFmpegHelper.getFFmpegVersion() ?? "Unknown version"
        
        
        let ffmpegWrapper =  FFmpegWrapper()
        print("Running objc-lib")
        ffmpegWrapper.runFFmpegCommand("Hewwo")
        
    }
    
    
    
}
