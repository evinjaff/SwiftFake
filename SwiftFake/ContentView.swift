//
//  ContentView.swift
//  SwiftFake
//
//  Created by Evin Jaff on 10/2/24.
//

import SwiftUI


struct ContentView: View {
    
    @State private var showingRecoridng = false
    @State private var showingConverter = false
    
    var body: some View {
        VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("Hello, world!")
        }
        .padding()
        
        Button("Show Recording Modal") {
            showingRecoridng.toggle()
        }
        .sheet(isPresented: $showingRecoridng) {
          RecorderView()
        }
        
        Button("Show Converter Modal") {
            showingConverter.toggle()
        }
        .sheet(isPresented: $showingConverter) {
          ConverterView()
        }
        
        
    }
}

#Preview {
    ContentView()
}
