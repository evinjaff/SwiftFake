//
//  ConverterView.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/3/24.
//

import SwiftUI
import CoreAudioTypes


extension AudioRecording {
    static let emptySelection = AudioRecording(url: URL(string: "https://example.com/audio0.mp3")!, directory: URL(string: "https://example.com")!, nickname: "No Recording")
}

struct ConverterView: View {
    
    @State var model: ConverterViewModel = ConverterViewModel()
    @State private var selectedRecording: AudioRecording = .emptySelection
    
    
    // Fetch the available audio recordings
    
    
    var body: some View {
        
        VStack{

            Picker("Select an Audio Recording", selection: $selectedRecording) {
                ForEach(model.audioRecordings, id:\.self) { recording in
                    Text(recording.nickname)
                        .tag(recording)
                }
            }
            .pickerStyle(MenuPickerStyle()) // You can change the picker style as needed
            
        }
        .onAppear {
            model.fetchAvailableAudioRecordings()
        }
        
        
        Text("Value of current selection: \(selectedRecording.nickname)")
        
        
        Button("Convert Recording to Deepfake-understandable format") {
            
            model.transcodeAudio(source: selectedRecording)
            
        }
        
        
        
        
    }
    

    

    
}

#Preview {
    ConverterView()
}
