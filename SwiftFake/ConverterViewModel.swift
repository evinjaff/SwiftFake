//
//  ConverterViewModel.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/3/24.
//

import Foundation
import CoreML
import RosaKit
import AVFAudio

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
    
    func runModelOnOutput(pathOfWav: URL) {
        
        let rmh = RTVCModelHandler()
        
        rmh.preProcessInput(wavFile: pathOfWav)

        
        
    }
    

    
}


// Assuming your CoreML model is named "RTVC"
class RTVCModelHandler {

    init() {

    }
    
    func preProcessInput(wavFile: URL) {
        
        var wfm = WavFileManager()
        // read wav file
        
        var wavFileComplete = URL(filePath: wavFile.path() + "output_audio.wav")
        
        do {
            print("reading audio from \(wavFile)")
            
            let data = try Data.init(contentsOf: wavFileComplete)
            
            let chunkSize = 66000
            let chunkOfSamples = data.float32Array
            
            let chunkOfDoubleSamples = chunkOfSamples.map {Double($0) ?? 0}
            
            let spectrogram = chunkOfDoubleSamples.stft()
            
            print(spectrogram)
            
            
            
        }
        catch {
            print("Error info: \(error)")
            print("Error reading wav file")
        }
        
    }


    


    // Function to make predictions with the model
    func predict(input: MLMultiArray) -> MLMultiArray? {
        do {
            // Create an instance of the input to pass to the model
            let modelInput = RTVCInput(utterances: input)

            // Return the output of the prediction
            return nil
        } catch {
            print("Error during prediction: \(error)")
            return nil
        }
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
