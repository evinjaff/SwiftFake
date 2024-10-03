//
//  RecorderView.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/2/24.
//

import AVFoundation
import Photos
import SwiftUI

struct RecorderView : View {
    
    @State private var viewModel: RecorderViewModel = RecorderViewModel()
    
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        
        VStack {
            Text(viewModel.name)
            
            
            Button("press to dismiss modal") {
                dismiss()
            }
            .font(.title2)
            .padding()
            
            Button (viewModel.isRecording ? "Stop Recording" : "Start Recording") {
                if (viewModel.isRecording) {
                    viewModel.stopRecording()
                }
                else {
                    viewModel.startRecording()
                }
            }
            .buttonStyle(.borderedProminent)
            .tint(viewModel.isRecording ? .red : .blue)
            
            
            Text("DEBUG Options")
            
            
            Button("Get filetype") {
                print(viewModel.getFile())
            }
            
            Button("DEBUG: File info") {
                let url = viewModel.getFile()
                print("path: .....\(url.lastPathComponent)")
                let exists = FileManager.default.fileExists(atPath: url.path)
                print("exists: \(exists)")
                if !exists { return }
                guard let attr = try? FileManager.default.attributesOfItem(atPath: url.path)
                else { print("couldn't get attributes"); return }
                guard let bytes = attr[.size] as? Int64
                else { print("no size???"); return }
                print("bytes: \(bytes)")
            }

            
        }
        
    }
    
    
}
