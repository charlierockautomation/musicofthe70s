// Cloudflare Pages serves the repo root, so internal working files
// (trackers, strategy, session archives, Claude skills, build scripts)
// would otherwise be public. Return a plain 404 for them; every other
// request falls through to the static site unchanged.
const BLOCKED_PREFIXES = ["/.claude/", "/scripts/", "/sources/", "/functions/", "/.git"];
const BLOCKED_ROOT_FILES = ["/quick_start.docx", "/quick_start.pdf", "/musicofthe70s_fixes.tar.gz", "/.gitignore"];

export function isBlocked(pathname) {
  let p;
  try { p = decodeURIComponent(pathname).toLowerCase(); } catch { return true; }
  if (p.endsWith(".md")) return true;
  if (BLOCKED_ROOT_FILES.includes(p)) return true;
  return BLOCKED_PREFIXES.some((prefix) => p.startsWith(prefix));
}

export async function onRequest(context) {
  if (isBlocked(new URL(context.request.url).pathname)) {
    return new Response("Not found", {
      status: 404,
      headers: { "content-type": "text/plain; charset=utf-8", "x-robots-tag": "noindex" },
    });
  }
  return context.next();
}
