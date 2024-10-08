//
//  ConverterViewModel.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/3/24.
//

import Foundation


// Filesystem traversal extensions
extension URL {
    var typeIdentifier: String? { (try? resourceValues(forKeys: [.typeIdentifierKey]))?.typeIdentifier }
    
    var isM4A: Bool { typeIdentifier == "com.apple.m4a-audio" }
    
    var localizedName: String? { (try? resourceValues(forKeys: [.localizedNameKey]))?.localizedName }
    var hasHiddenExtension: Bool {
        get { (try? resourceValues(forKeys: [.hasHiddenExtensionKey]))?.hasHiddenExtension == true }
        set {
            var resourceValues = URLResourceValues()
            resourceValues.hasHiddenExtension = newValue
            try? setResourceValues(resourceValues)
        }
    }
}


@Observable
class ConverterViewModel {
    
    var audioRecordings: [AudioRecording] = []
    
    func fetchAvailableAudioRecordings() -> Array<AudioRecording> {
        
        do {
            // Get the document directory url
            let documentDirectory = try FileManager.default.url(
                for: .documentDirectory,
                in: .userDomainMask,
                appropriateFor: nil,
                create: true
            )
            print("documentDirectory", documentDirectory.path)
            // Get the directory contents urls (including subfolders urls)
            let directoryContents = try FileManager.default.contentsOfDirectory(
                at: documentDirectory,
                includingPropertiesForKeys: nil
            )
            print("directoryContents:", directoryContents.map { $0.localizedName ?? $0.lastPathComponent })
//            for url in directoryContents {
//                print(url.localizedName ?? url.lastPathComponent)
//                print(url.typeIdentifier)
//            }

            // get all audio files
            let audio = directoryContents.filter(\.isM4A).map { $0.localizedName ?? $0.lastPathComponent }
            print("audio files:", audio)
            
            self.audioRecordings = directoryContents.filter(\.isM4A).map { AudioRecording(url: $0, directory: documentDirectory, nickname: $0.localizedName ?? $0.lastPathComponent) }
            
            return self.audioRecordings
            
        } catch {
            print(error)
        }
        
        
        return []

    }
    
    
    func fetchFFmpegVersion() {
        FFmpegWrapper.getFFmpegVersion()
        print("Running objc-lib")
    }
    
    
    func transcodeAudio(source: AudioRecording) {
        
        
        
        var input = source.url.path()
        var output = source.directory.path() + "output_audio.wav"
        
        print("Transcode i: \(input) \n o:\(output)")
        
        
        FFmpegWrapper.transcodeToPCM161e(withInput: input, output: output)
        
    }
    

    
}


struct AudioRecording: Identifiable, Hashable {
    var id: UUID = UUID()
    
    var url: URL
    var nickname: String
    // url to base directory where file is
    var directory: URL
    
    
    init(url: URL, directory: URL, nickname: String) {
        self.url = url
        self.directory = directory
        self.nickname = nickname
        
    }
    
    
}
