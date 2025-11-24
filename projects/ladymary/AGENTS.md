# LadyMary.com - Project Instructions

> WordPress-based website

---

## Stack Tecnico

| Component | Technology |
|-----------|------------|
| CMS | WordPress |
| Language | PHP |
| Database | MySQL/MariaDB |
| Web Server | Nginx |

---

## File Structure

```
/var/www/ladymary.com/
├── index.php           # WordPress entry point
├── wp-config.php       # WP configuration (if standard WP)
├── wp-content/         # Themes, plugins, uploads
├── wp-admin/           # Admin dashboard
├── wp-includes/        # Core WordPress files
└── .htaccess           # Apache rules (if applicable)
```

---

## Comandi Rapidi

```bash
# Check PHP version
php -v

# Check WordPress CLI (if installed)
wp --info

# Database backup
mysqldump -u user -p ladymary_db > backup.sql

# Check file permissions
ls -la /var/www/ladymary.com/
```

---

## WordPress Admin

- **URL**: https://ladymary.com/wp-admin
- **Login**: Check wp-config.php or ask admin

---

## Common Tasks

### Update WordPress
```bash
# Via WP-CLI
wp core update
wp plugin update --all
wp theme update --all
```

### Clear Cache
```bash
# If using cache plugin
wp cache flush

# Clear nginx cache
sudo find /var/cache/nginx -type f -delete
sudo systemctl reload nginx
```

### Debug Mode
In `wp-config.php`:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

Logs in: `wp-content/debug.log`

---

## Security

- Keep WordPress updated
- Use strong admin passwords
- Limit login attempts
- Regular backups
- Disable file editing:
  ```php
  define('DISALLOW_FILE_EDIT', true);
  ```

---

## Troubleshooting

### White Screen of Death
```bash
# Check PHP errors
tail -50 /var/log/nginx/error.log
tail -50 /var/log/php-fpm/error.log

# Enable debug mode
# Edit wp-config.php → WP_DEBUG = true
```

### Database Connection Error
```bash
# Check MySQL
systemctl status mysql

# Test connection
mysql -u wp_user -p -h localhost wp_database
```

### Permission Issues
```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/ladymary.com
sudo find /var/www/ladymary.com -type d -exec chmod 755 {} \;
sudo find /var/www/ladymary.com -type f -exec chmod 644 {} \;
```

---

## Nginx Config

Typical WordPress nginx config location:
```
/etc/nginx/sites-enabled/ladymary.com
```

Test and reload:
```bash
nginx -t && sudo systemctl reload nginx
```
