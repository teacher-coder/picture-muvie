import { describe, it, expect } from "vitest";
import { compressLyrics } from "./utils";

const SAMPLE_LYRICS = `Test me test me
Freedom
Test me test me
Freedom
어디서도 볼 수 없었던 이상한 놈이 나야 Ooh ah
남들이 하자고 하는 건 이상하게 흥미 없지 Ooh ah
부르지 마
I love it now
혹시 내가 뭔가 아쉬워 보이나
제발 관심 끄고 너희 걱정이나 하라고
Yes I'm a freak
다들 똑같이
웃을 때 웃지 못하는 걸
답은 정해져 있지만
자 해봐 You can test me
내가 할 거 같애 안할 거 같애?
이보다 완벽할 수 있다면 날 데려가 봐
Test me test me
이보다 재밌을 수 있다면 날 데려가 봐
Test me test me`;

function countLines(text: string): number {
  return text.split("\n").filter((n) => n).length;
}

describe("compressLyrics", () => {
  it("should return fewer lines with higher offset", () => {
    const lines10 = countLines(compressLyrics(SAMPLE_LYRICS, 10));
    const lines50 = countLines(compressLyrics(SAMPLE_LYRICS, 50));
    expect(lines50).toBeLessThanOrEqual(lines10);
  });

  it("should not lose content when compressing", () => {
    const original = SAMPLE_LYRICS.replace(/\s+/g, " ").trim();
    const compressed = compressLyrics(SAMPLE_LYRICS, 30)
      .replace(/\s+/g, " ")
      .trim();
    expect(compressed).toBe(original);
  });

  it("original sample has 20 lines", () => {
    expect(countLines(SAMPLE_LYRICS)).toBe(20);
  });
});

describe("compressToTargetLines (simulation)", () => {
  // Simulate the compressToTargetLines logic from Home.tsx
  function compressToTargetLines(lyricText: string, target: number): string {
    for (let o = 1; o <= 100; o++) {
      const compressed = compressLyrics(lyricText, o);
      if (countLines(compressed) <= target) {
        return compressed;
      }
    }
    return lyricText;
  }

  const targets = [5, 10, 15, 20, 24, 30];

  for (const target of targets) {
    it(`target ${target} lines → actual lines should be <= ${target}`, () => {
      const result = compressToTargetLines(SAMPLE_LYRICS, target);
      const actual = countLines(result);
      console.log(`  target: ${target}, actual: ${actual}`);
      expect(actual).toBeLessThanOrEqual(target);
    });
  }

  it("target 20 should return exact or close to 20", () => {
    const result = compressToTargetLines(SAMPLE_LYRICS, 20);
    const actual = countLines(result);
    // Since original is 20 lines, it should stay 20
    expect(actual).toBe(20);
  });

  it("target 10 should not return more than 10", () => {
    const result = compressToTargetLines(SAMPLE_LYRICS, 10);
    const actual = countLines(result);
    expect(actual).toBeLessThanOrEqual(10);
    // But also not too few — should be reasonably close
    console.log(`  target: 10, actual: ${actual}, gap: ${10 - actual}`);
  });
});
