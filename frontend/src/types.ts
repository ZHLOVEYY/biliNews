export interface VideoInfo {
  title: string
  bvid: string
  cover: string
  duration: string
  play_count: number
  danmaku_count: number
  url: string
  description: string
}

export interface VideoAnalysis {
  summary: string
  quality_assessment: string
}

export interface VideoResult {
  video_info: VideoInfo
  analysis: {
    video_analysis: VideoAnalysis
  }
}