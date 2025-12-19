# SPRINT 7 Реализация функций безопасного вывода ключей из паролей и мастер-ключей

## 1. PBKDF2-HMAC-SHA256
Спецификация: RFC 2898

Алгоритм: HMAC-SHA256

Итерации: До 1,000,000+

Длина ключа: Любая (1-100+ байт)

Соль: Поддержка hex-строк и автогенерации

## 2. Иерархия ключей (HKDF-стиль)
Функция: derive_key(master_key, context, length)

Контекст: Уникальный идентификатор назначения ключа

Детерминированность: Одинаковые входы → одинаковые выходы

Разделение: Разные контексты → разные ключи


## Опция	            Описание
--password	      Парольная строка	
--password-file   Файл с паролем	
--salt	          Соль в hex-формате
--iterations	    Количество итераций
--length	        Длина ключа в байтах
--algorithm	      Алгоритм KDF	
--output	        Файл для сохранения ключа	
--output-salt	    Файл для сохранения соли	

## Минимальные требования:
Итерации: Минимум 100,000 для PBKDF2

Соль: Всегда уникальная, случайная (16+ байт)

Пароль: Сильный, сложный пароль

Хранение: Храните производные ключи, а не пароли

Базовые команды:
1. Деривация с указанной солью:

```bash
cryptocore derive --password "MySecurePassword123!" --salt a1b2c3d4e5f60123456789012345678
```
2. Деривация с автогенерацией соли:

```bash
cryptocore derive --password "AnotherPassword" --iterations 500000 --length 16
```
3. Сохранение ключа в файл:

```bash
cryptocore derive --password "app_key" --salt fixedappsalt --iterations 10000 --length 32 --output app_key.bin
```

4. Чтение пароля из файла:
```bash
# Создайте файл с паролем
echo "MySecretPassword" > password.txt
# Используйте его для деривации
cryptocore derive --password-file password.txt --salt 1234567890abcdef
```

Различные длины ключей:

```bash
# Короткий ключ (1 байт)
cryptocore derive --password "test" --salt 1234 --length 1

# Стандартный ключ (16 байт)
cryptocore derive --password "test" --salt 1234 --length 16

# Длинный ключ (64 байта)
cryptocore derive --password "test" --salt 1234 --length 64

# Очень длинный ключ (100 байт)
cryptocore derive --password "test" --salt 1234 --length 100
```
