//
//  RecorderViewModel.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/2/24.
//

import Foundation
import Combine
import SwiftUI
import AVFoundation


@Observable
class RecorderViewModel {
    private(set) var numRecordings: Int32
    private(set) var name : String
    
    var recorder: AVAudioRecorder? = nil
    let session_var = AVAudioSession.sharedInstance()
    var isRecording = false
    
    init() {
        do {
            numRecordings = 0
            name = "RecorderView"
        } catch {
            name = "Error"
        }
    }
    
    func startRecording() {
        let settings = [
            AVFormatIDKey: Int(kAudioFormatMPEG4AAC),
            AVSampleRateKey: 12000,
            AVNumberOfChannelsKey: 1,
            AVEncoderAudioQualityKey: AVAudioQuality.high.rawValue
        ]
        
        do {
            try session_var.setCategory(.record, mode: .default)
            try session_var.setActive(true)
            let r = try AVAudioRecorder(url: getFile(), settings: settings)
            let b: Bool = r.record()
            recorder = r
            isRecording = true
            print("recording started, b: \(b)")
        } catch {
            print("recording start failed")
        }
        
    }
    
    func stopRecording() {
        guard let r = recorder else { print("Error: Not Recording"); return }
        do {
            r.stop()
            recorder = nil
            try session_var.setActive(false)
            isRecording = false
            print("recording stopped")
        } catch {
            print("recording stop failed")
        }
        
    }
    
    func getFile() -> URL {
        let path = FileManager.default.urls(for: .documentDirectory, in:.userDomainMask)
        return path[0].appendingPathComponent("recording.m4a")
    }
    
    
}



