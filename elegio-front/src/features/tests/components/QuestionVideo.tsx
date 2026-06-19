type QuestionVideoProps = {
  url: string
}

function tiktokId(url: string): string | null {
  return url.match(/\/video\/(\d+)/)?.[1] ?? null
}

function youtubeId(url: string): string | null {
  return (
    url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([\w-]+)/)?.[1] ??
    null
  )
}

/**
 * Renders the video attached to a question. Supports TikTok and YouTube via
 * their embed players, falling back to a native <video> for direct files.
 */
export function QuestionVideo({ url }: QuestionVideoProps) {
  const tiktok = tiktokId(url)
  const youtube = tiktok ? null : youtubeId(url)

  if (tiktok) {
    return (
      <div className="mx-auto aspect-[9/16] w-full max-w-[20rem] overflow-hidden rounded-3xl bg-black">
        <iframe
          src={`https://www.tiktok.com/player/v1/${tiktok}`}
          title="Video de la pregunta"
          className="h-full w-full"
          allow="autoplay; fullscreen; encrypted-media; picture-in-picture"
          allowFullScreen
        />
      </div>
    )
  }

  if (youtube) {
    return (
      <div className="mx-auto aspect-video w-full max-w-2xl overflow-hidden rounded-3xl bg-black">
        <iframe
          src={`https://www.youtube.com/embed/${youtube}`}
          title="Video de la pregunta"
          className="h-full w-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowFullScreen
        />
      </div>
    )
  }

  return (
    <video
      controls
      src={url}
      className="mx-auto w-full max-w-2xl rounded-3xl bg-black"
    />
  )
}
