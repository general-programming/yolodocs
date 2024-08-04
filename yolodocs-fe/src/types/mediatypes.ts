export enum MediaType {
  IMAGE = 'image',
  VIDEO = 'video'
}

export type MediaItem = {
  created: string
  file_id: number
  filename: string
  media_height: number
  media_length: number
  media_length_ms: number
  media_type: MediaType
  media_width: number
  mime: string
  size: number
  transcript: string
}

export type PaginatedResult = {
  pages: number
  total: number
}

export type MediaListResult = PaginatedResult & {
  items: MediaItem[]
}
