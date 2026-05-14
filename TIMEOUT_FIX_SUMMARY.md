# Timeout Error Fix

## Problem
- Frontend was getting "timeout of 60000ms exceeded" errors
- LLM operations (Ollama) can take longer than 60 seconds

## Solution Applied

### 1. Increased Timeouts
- **Default timeout**: 60s → 120s (2 minutes)
- **LLM endpoints** (`/generate-sql`, `/optimize-query`): 180s (3 minutes)

### 2. Better Error Handling
- Added specific timeout error detection
- User-friendly error messages
- Suggests checking Ollama status

## Files Changed
1. `frontend/src/api/apiClient.js`
   - Increased default timeout to 120s
   - Added 180s timeout for LLM endpoints

2. `frontend/src/components/QueryAssistant.jsx`
   - Added timeout-specific error handling
   - Better error messages for users

## Troubleshooting

If you still get timeouts:

1. **Check Ollama is running**:
   ```bash
   ollama list
   ```

2. **Check if model is available**:
   ```bash
   ollama show gemma3:4b
   ```

3. **Test Ollama directly**:
   ```bash
   ollama run gemma3:4b "Hello"
   ```

4. **Check backend logs** for LLM errors

5. **Restart backend** if needed

## Notes
- LLM operations are inherently slow (especially first call)
- 3 minutes should be enough for most queries
- If still timing out, Ollama might be slow or unresponsive
