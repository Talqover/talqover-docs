# Multi-Language Documentation Guide

## Overview

The Talkover documentation now supports both English (EN) and Brazilian Portuguese (PT-BR) languages. This guide explains how to maintain and update the documentation in both languages.

## Quick Start

### Running the Documentation

```bash
# Start development server
mint dev

# The documentation will be available at:
# - English: http://localhost:3000/en
# - Portuguese: http://localhost:3000/pt-br
```

### Language Switching

Users can switch between languages using the language selector in the navigation bar. The default language is English.

## File Structure

```
talkover-docs/
├── en/                    # English content
│   ├── introduction.mdx
│   ├── essentials/
│   │   ├── code.mdx
│   │   ├── images.mdx
│   │   ├── markdown.mdx
│   │   ├── navigation.mdx
│   │   ├── reusable-snippets.mdx
│   │   └── settings.mdx
│   └── api-reference/
│       └── introduction.mdx
├── pt-br/                 # Portuguese content
│   ├── introduction.mdx
│   ├── essentials/
│   │   ├── code.mdx
│   │   ├── images.mdx
│   │   ├── markdown.mdx
│   │   ├── navigation.mdx
│   │   ├── reusable-snippets.mdx
│   │   └── settings.mdx
│   └── api-reference/
│       └── introduction.mdx
├── api-reference/         # Shared OpenAPI files
│   ├── openapi.json
│   └── endpoint/
├── images/               # Shared images
├── logo/                 # Shared logos
├── docs.json            # Main configuration
└── development.mdx      # Development guide
```

## Adding New Content

### Step 1: Create English Version

1. Create the English content in the `en/` directory
2. Use proper MDX frontmatter with title and description
3. Follow the existing naming conventions

Example:
```mdx
---
title: "New Feature Guide"
description: "Learn how to use the new feature"
---

# New Feature Guide

Content here...
```

### Step 2: Create Portuguese Version

1. Create the Portuguese content in the `pt-br/` directory
2. Use the same file name and structure
3. Translate the content appropriately

Example:
```mdx
---
title: "Guia da Nova Funcionalidade"
description: "Aprenda como usar a nova funcionalidade"
---

# Guia da Nova Funcionalidade

Conteúdo aqui...
```

### Step 3: Update Navigation

Update the `docs.json` file to include the new pages in both language sections:

```json
{
  "navigation": {
    "languages": [
      {
        "language": "en",
        "groups": [
          {
            "group": "New Section",
            "pages": [
              "en/new-feature-guide"
            ]
          }
        ]
      },
      {
        "language": "pt-BR",
        "groups": [
          {
            "group": "Nova Seção",
            "pages": [
              "pt-br/new-feature-guide"
            ]
          }
        ]
      }
    ]
  }
}
```

## Translation Guidelines

### Technical Terms

Keep technical terms consistent across languages:

| English | Portuguese |
|---------|------------|
| API | API |
| Endpoint | Endpoint |
| Authentication | Autenticação |
| Bearer Token | Token Bearer |
| Rate Limit | Limite de Taxa |
| Webhook | Webhook |

### Content Structure

- Maintain the same heading structure
- Keep the same code examples (only translate comments if needed)
- Use the same component structure
- Ensure all links point to the correct language version

### Links Between Pages

When linking between pages, use language-specific paths:

```mdx
<!-- English -->
[API Reference](/en/api-reference/introduction)

<!-- Portuguese -->
[Referência da API](/pt-br/api-reference/introduction)
```

## Best Practices

### 1. Content Synchronization

- Always create content for both languages
- Keep content synchronized between versions
- Update both languages when making changes

### 2. File Naming

- Use consistent file names across language folders
- Use kebab-case for file names
- Keep names descriptive and meaningful

### 3. Testing

- Test both languages before deploying
- Verify all links work in both languages
- Check that navigation is correct for both languages

### 4. SEO

- Use appropriate meta descriptions for each language
- Include language-specific keywords
- Ensure proper alt text for images in both languages

## Common Tasks

### Adding a New Page

1. Create `en/new-page.mdx`
2. Create `pt-br/new-page.mdx`
3. Update `docs.json` navigation
4. Test both languages locally
5. Deploy

### Updating Existing Content

1. Update English version first
2. Update Portuguese version to match
3. Test both languages
4. Deploy

### Adding New Navigation Groups

1. Add group to English navigation in `docs.json`
2. Add corresponding group to Portuguese navigation
3. Create content for both languages
4. Test navigation structure

## Troubleshooting

### Language Not Showing

- Check that the language is properly configured in `docs.json`
- Verify the language code is correct (e.g., "pt-BR" not "pt")
- Ensure the language has at least one group with pages

### Broken Links

- Use `mint broken-links` to check for broken links
- Verify all internal links use the correct language prefix
- Check that external links are accessible

### Content Not Updating

- Clear browser cache
- Restart the development server
- Check file permissions and paths

## Deployment

When deploying:

1. Build the documentation: `mint build`
2. Verify both languages are included in the build
3. Test the deployed site in both languages
4. Check that language switching works correctly

## Support

For issues with the multi-language setup:

1. Check the [Mintlify documentation](https://mintlify.com/docs)
2. Review the `development.mdx` file
3. Contact the development team

---

**Remember**: Always maintain both languages when making changes to ensure a consistent experience for all users.
