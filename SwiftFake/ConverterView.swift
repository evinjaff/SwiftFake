//
//  ConverterView.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/3/24.
//

import SwiftUI
import CoreAudioTypes



struct ConverterView: View {
    @State var model : ConverterViewModel = ConverterViewModel()
    
    var body: some View {
        
        
        Text(/*@START_MENU_TOKEN@*/"Hello, World!"/*@END_MENU_TOKEN@*/)
        
        Button("Click to test ffmpeg") {
            print("Going to run fetchffmpegversion")
            model.fetchFFmpegVersion()
        }
        .buttonStyle(.borderedProminent)
        
    }
}

#Preview {
    ConverterView()
}
