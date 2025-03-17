export interface VideoInfo {
  title: string
  cover: string
  play_count: number
  danmaku_count: number
  duration: string
  url: string
}

export interface AnalysisData {
  summary: string
  quality_assessment: string
}

export interface VideoResult {
  video_info: VideoInfo
  analysis: {
    video_analysis: AnalysisData
  }
}