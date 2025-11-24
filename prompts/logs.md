# /logs

Visualizza e analizza log di un servizio specifico.

## Argomenti

- `$1`: nome del servizio (es. `api`, `nginx`, `postgresql`, `mcp-server`)
- `$2`: (opzionale) numero di linee (default: 100)
- `$3`: (opzionale) filtro grep (es. "ERROR", "CRITICAL")

## Istruzioni

### Log Mapping

| Servizio | Comando |
|----------|---------|
| api | `journalctl -u api.service -n $LINES --no-pager` |
| nginx | `tail -n $LINES /var/log/nginx/error.log` |
| nginx-access | `tail -n $LINES /var/log/nginx/access.log` |
| postgresql | `journalctl -u postgresql -n $LINES --no-pager` |
| mcp-server | `journalctl -u mcp-server.service -n $LINES --no-pager` |
| gunicorn | `tail -n $LINES /var/log/aiagens/gunicorn-error.log` |

### Esecuzione

1. Determina il comando corretto dal mapping
2. Esegui con le opzioni specificate
3. Se `$3` (filtro) presente, applica grep
4. Evidenzia errori critici nell'output

### Analisi Automatica

Se trovi errori:
- Raggruppa errori simili
- Identifica pattern (es. errori ripetuti ogni X minuti)
- Suggerisci possibile causa

## Output

```
## Logs: $1 (ultime $2 linee)

[Output log, troncato se necessario]

## Analisi

**Errori trovati**: X
**Pattern identificati**: [se presenti]
**Suggerimento**: [se applicabile]
```
