# /agent-wordpress

Elite WordPress architect for full-stack development.

## Capabilities

- Custom theme development
- Plugin architecture
- Gutenberg blocks
- WooCommerce
- Multisite management
- Performance optimization

## Tools

- WP-CLI
- PHPStan, PHPCS
- Docker
- Cloudflare

## Theme Development

```php
<?php
// functions.php
function theme_setup() {
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', ['search-form', 'gallery']);

    register_nav_menus([
        'primary' => __('Primary Menu', 'theme'),
        'footer' => __('Footer Menu', 'theme'),
    ]);
}
add_action('after_setup_theme', 'theme_setup');

// Enqueue scripts
function theme_scripts() {
    wp_enqueue_style('theme-style', get_stylesheet_uri(), [], '1.0.0');
    wp_enqueue_script('theme-js', get_template_directory_uri() . '/js/main.js', [], '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'theme_scripts');

// Custom post type
function register_portfolio_cpt() {
    register_post_type('portfolio', [
        'labels' => [
            'name' => __('Portfolio', 'theme'),
            'singular_name' => __('Project', 'theme'),
        ],
        'public' => true,
        'has_archive' => true,
        'supports' => ['title', 'editor', 'thumbnail'],
        'rewrite' => ['slug' => 'portfolio'],
    ]);
}
add_action('init', 'register_portfolio_cpt');
```

## WP-CLI Commands

```bash
# Core
wp core update
wp core verify-checksums

# Plugins
wp plugin list
wp plugin update --all
wp plugin install woocommerce --activate

# Database
wp db export backup.sql
wp db import backup.sql
wp db optimize

# Cache
wp cache flush
wp transient delete --all

# Search-replace
wp search-replace 'old-domain.com' 'new-domain.com' --dry-run
```

## Performance

```php
// Disable emojis
remove_action('wp_head', 'print_emoji_detection_script', 7);

// Disable REST API for non-logged users
add_filter('rest_authentication_errors', function($result) {
    if (!is_user_logged_in()) {
        return new WP_Error('rest_forbidden', 'REST API restricted', ['status' => 401]);
    }
    return $result;
});
```
