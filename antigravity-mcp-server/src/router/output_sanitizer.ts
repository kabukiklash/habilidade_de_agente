/**
 * LLM Router — Output Sanitizer
 *
 * Protects Claude against prompt injection from external LLM responses.
 * Gap identified in OpenClaude analysis: zero sanitization on MCP output.
 *
 * Threat model:
 *   1. Prompt injection — LLM output crafted to override Claude's behavior
 *   2. Role hijacking — attempts to redefine Claude's identity or role
 *   3. Token bombing — oversized outputs consuming excessive context
 *   4. Delimiter injection — fake system/human tags in response text
 */

export interface SanitizeResult {
  safe: boolean;
  content: string;
  warnings: string[];
  originalLength: number;
}

// Patterns that indicate prompt injection attempts
const INJECTION_PATTERNS: Array<{ pattern: RegExp; label: string }> = [
  { pattern: /ignore\s+(all\s+)?previous\s+instructions?/gi,     label: "instruction_override" },
  { pattern: /forget\s+(everything|all\s+previous)/gi,            label: "instruction_override" },
  { pattern: /new\s+instructions?\s*:/gi,                         label: "instruction_injection" },
  { pattern: /you\s+are\s+now\s+(a\s+|an\s+)?(?!the\s+same)/gi, label: "role_hijack" },
  { pattern: /\[SYSTEM\]/gi,                                       label: "delimiter_injection" },
  { pattern: /\[INST\]|\[\/INST\]/gi,                             label: "delimiter_injection" },
  { pattern: /<\|system\|>|<\|user\|>|<\|assistant\|>/gi,        label: "delimiter_injection" },
  { pattern: /OVERRIDE\s*:/gi,                                     label: "instruction_override" },
  { pattern: /###\s*System\s*:/gi,                                 label: "delimiter_injection" },
  { pattern: /act\s+as\s+(if\s+you\s+are|a)\s+(?!an?\s+expert)/gi, label: "role_hijack" },
];

// Maximum characters allowed in sanitized output
const MAX_OUTPUT_CHARS = 8_000;

// Minimum content length — reject suspiciously empty responses
const MIN_OUTPUT_CHARS = 1;

export function sanitizeOutput(
  raw: string,
  providerName: string,
): SanitizeResult {
  const warnings: string[] = [];
  const originalLength = raw.length;
  let content = raw;

  // 1. Token bomb protection — truncate before any pattern matching
  if (content.length > MAX_OUTPUT_CHARS) {
    content = content.slice(0, MAX_OUTPUT_CHARS) + "\n\n[OUTPUT TRUNCATED BY SANITIZER]";
    warnings.push(
      `token_bomb: output truncated ${originalLength} → ${MAX_OUTPUT_CHARS} chars (provider=${providerName})`,
    );
  }

  // 2. Prompt injection detection and redaction
  for (const { pattern, label } of INJECTION_PATTERNS) {
    if (pattern.test(content)) {
      content = content.replace(pattern, "[REDACTED]");
      warnings.push(`injection_detected: pattern=${label} provider=${providerName}`);
    }
  }

  // 3. Empty / useless response guard
  if (content.trim().length < MIN_OUTPUT_CHARS) {
    warnings.push(`empty_response: provider=${providerName} returned blank content`);
  }

  return {
    safe: warnings.length === 0,
    content,
    warnings,
    originalLength,
  };
}
