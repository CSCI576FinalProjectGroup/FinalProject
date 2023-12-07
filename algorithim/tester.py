#!/usr/bin/env python3

import main_algorithim

def run_test_for_all_clips():
	clips = [
		'/Users/arshiabehzad/Downloads/Videos/video1_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video2_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video3_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video4_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video5_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video6_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video7_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video8_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video9_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video10_1.mp4',
		'/Users/arshiabehzad/Downloads/Videos/video11_1.mp4'
	]
	
	for clip in clips:
		clip_rgb = clip.replace('.mp4', '.rgb')
		print(f"Testing {clip}")
		main_algorithim.main(clip, clip_rgb)
		print("\n")
		
if __name__ == "__main__":
	run_test_for_all_clips()