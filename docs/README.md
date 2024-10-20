# SwiftFake: Real-time Defense against Adversarial Voice Cloning

This site is the page for all information and updates about my Master's Capstone SwiftFake, which aims to build a real-time defense against attacks using Adversarial Cloning or "Deepfakes".


## Gap in Literature

Through a search of academic literature, I identified that local real-time deepfake audio detection was a missing area of study in academia, with many papers requring a PC or offloading compute to a server. There has been a significant lack of engineering work exploring performance, with most of the existing work running models on high-power GPUs that draw 15-40x the power of a smartphone and lacked scalability.

## Existing Work by Lab

Our lab had previously won the FTC Voice Cloning Challenge award for the paper [AntiFake](https://github.com/WUSTL-CSPL/AntiFake?tab=readme-ov-file), which focuesd on preventing a user's voice recording from being deepfaked by training perturbations optimized against the loss functions of popular voice deepfake encoders like RTVC. Due to this paper, our lab also consulted with The White House this year about how to prevent the spread of deepfakes related to the 2024 election. While this existing work was promising, it lacked scalability in the mobile domain- requiring an Nvidia GPU with at least 8 GB of VRAM, took a lot of time to run, and needed a complete audio clip to train effective perturbations.


## Code and Algorithm

Coming soon in November!

## Threat Model

The threat model is as follows, a user through a voice calling app is communicating with someone who has deepfaked their voice to impersonate a credible person (i.e. a relative, friend, politician, etc. ). The adversary is trying to convince the victim to perform an action by using the credibility of the deepfaked voice.

## FAQ

### What devices can SwiftFake run on?

Depending on engineering, either on iOS or Android. Currently, it is on iOS (hence the clever pun SwiftFake) but may be changed to Android depending on if there are any API issues.


### Can I watch a talk on SwiftFake?

I will be defending SwiftFake for my MS capstone on December 12th, 2024. I will stream a feed of on YouTube (pending department persmisson). Additionally, I will post a recording of my defense on YouTube to be watched afterwards that I will link here. I also plan to submit a paper to USENIX 2025 and may deliver a talk there.



