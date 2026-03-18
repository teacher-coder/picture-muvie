const API_BASE = import.meta.env.VITE_API_URL || "/";

export interface LyricsResponse {
  source: string;
  title: string;
  artist: string;
  lyrics: string;
}

export async function getLyrics(query: string): Promise<LyricsResponse> {
  const res = await fetch(
    `${API_BASE}api/lyrics?query=${encodeURIComponent(query)}`
  );
  if (!res.ok) throw new Error("검색 실패");
  return res.json();
}

export async function downloadLyricsDocx(
  title: string,
  lyrics: string[]
): Promise<Blob> {
  const res = await fetch(`${API_BASE}api/makedocx`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, lyrics }),
  });
  if (!res.ok) throw new Error("다운로드 실패");
  return res.blob();
}
