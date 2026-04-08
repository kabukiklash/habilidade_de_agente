/**
 * Tool: read_file_smart
 * Reads a file with automatic compression for large files (> max_lines).
 *
 * Does NOT depend on CMS — purely local file operation.
 * Delegates to read_smart.py from the Cognitive Kit which:
 *   - Returns full content for files <= max_lines
 *   - Returns compressed skeleton (imports, class/def) for larger files
 *   - Updates the MD5 cache automatically
 *
 * Token savings: 30–60% on files > 120 lines.
 */

import { spawnSync } from "child_process";
import * as fs from "fs";

const READ_SMART_PATH =
  "C:/Users/RobsonSilva-AfixGraf/claude-cognitive-kit/read_smart.py";

const DEFAULT_MAX_LINES = 120;

export async function readFileSmart(params: unknown): Promise<object> {
  const p = params as Record<string, unknown>;
  const file_path = p.file_path as string;
  const max_lines =
    typeof p.max_lines === "number" ? p.max_lines : DEFAULT_MAX_LINES;

  // Input validation
  if (!file_path || typeof file_path !== "string") {
    return { error: "INVALID_INPUT", reason: "file_path is required" };
  }

  if (!fs.existsSync(file_path)) {
    return { error: "FILE_NOT_FOUND", reason: `File not found: ${file_path}` };
  }

  // Delegate to Python read_smart.py
  const result = spawnSync(
    "python",
    [READ_SMART_PATH, file_path, String(max_lines)],
    { encoding: "utf-8", timeout: 15000 }
  );

  if (result.error) {
    return { error: "SPAWN_ERROR", reason: result.error.message };
  }

  if (result.status !== 0) {
    return {
      error: "PYTHON_ERROR",
      reason: result.stderr || "Unknown error from read_smart.py",
      exit_code: result.status,
    };
  }

  const output = result.stdout ?? "";
  const firstLine = output.split("\n")[0] ?? "";
  const compressed = firstLine.includes("COMPRIMIDO:");

  // Extract savings pct from header comment if compressed
  let savings_pct: number | null = null;
  const match = firstLine.match(/COMPRIMIDO:\s*([\d.]+)%/);
  if (match) savings_pct = parseFloat(match[1]);

  return {
    status: "ok",
    file_path,
    compressed,
    savings_pct,
    summary: firstLine,
    content: output,
  };
}
