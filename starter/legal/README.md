# legal/ — plantillas legales (adáptalas)

> 🌐 Versión en inglés de las plantillas en `en/` (`legal/en/*.md`). El pipeline renderiza
> las del idioma de `site.language` (si existe `legal/en/`, para un medio en inglés).

> ⚠️ **NO es asesoría legal.** Son plantillas base para que tu medio arranque con lo
> mínimo razonable. **Adáptalas a tu caso y a tu jurisdicción** y, si vas en serio
> (recoges datos personales, monetizas, tratas temas sensibles), **consúltalas con un
> profesional.** Rellena los `<PLACEHOLDER>`. Referencia: 2026-08.

## Qué hay aquí

| Fichero | Para qué | ¿Cuándo la necesitas? |
|---|---|---|
| [privacidad.md](privacidad.md) | Política de privacidad (newsletter, datos) | En cuanto recojas **cualquier** dato (un email) |
| [divulgacion-ia.md](divulgacion-ia.md) | Declaración de que el contenido lo redacta una IA | Siempre (transparencia + AI Act UE) |
| [derechos-fuentes.md](derechos-fuentes.md) | Política de fuentes y proceso de retirada | Siempre (curas contenido de terceros) |
| [terminos.md](terminos.md) | Términos de uso del sitio | Recomendable antes de publicar |

## Cómo usarlas

1. Rellena los `<PLACEHOLDER>` (nombre del medio, dominio, responsable, email de contacto…).
2. Tu agente puede convertirlas en páginas del sitio y enlazarlas desde el footer.
3. Revisa la de **privacidad** con cuidado si tu público está en la UE (RGPD) o si vas a
   monetizar. Ver también [../../02-CUENTAS-Y-DOMINIO.md](../../02-CUENTAS-Y-DOMINIO.md).

## Checklist mínimo antes de publicar

- [ ] Footer enlaza **privacidad**, **divulgación de IA** y **derechos/retirada**.
- [ ] La newsletter usa **doble opt-in** y **baja con token firmado** (no `?email=` en plano).
- [ ] Hay un **email de contacto** real para retiradas y ejercicio de derechos.
- [ ] Ninguna afirmación inventada; cada hecho enlaza su fuente.
