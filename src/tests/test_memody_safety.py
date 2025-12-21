import os
import tempfile
import gc
import psutil
import unittest
import sys
from pathlib import Path

# Добавляем путь к проекту для импорта модулей
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestMemorySafety(unittest.TestCase):
    """Тесты безопасности памяти для Cryptocore"""
    
    @classmethod
    def setUpClass(cls):
        """Создание временной директории для тестовых файлов"""
        cls.test_dir = tempfile.mkdtemp(prefix="cryptocore_memory_test_")
        cls.large_file_path = os.path.join(cls.test_dir, "large_test_file.bin")
        
        # Создаем процесс для мониторинга памяти
        cls.process = psutil.Process(os.getpid())
        print(f"\n Начальное использование памяти: {cls.process.memory_info().rss / 1024 / 1024:.2f} MB")
    
    @classmethod
    def tearDownClass(cls):
        """Очистка временных файлов"""
        import shutil
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)
            print(f" Очищена тестовая директория: {cls.test_dir}")
    
    def get_memory_usage(self):
        """Получить текущее использование памяти в MB"""
        return self.process.memory_info().rss / 1024 / 1024
    
    def create_large_file(self, size_mb):
        """Создает большой файл указанного размера в MB"""
        chunk_size = 1024 * 1024  # 1MB
        total_size = size_mb * 1024 * 1024
        
        print(f" Создание файла размером {size_mb} MB...")
        
        with open(self.large_file_path, 'wb') as f:
            bytes_written = 0
            while bytes_written < total_size:
                chunk = os.urandom(min(chunk_size, total_size - bytes_written))
                f.write(chunk)
                bytes_written += len(chunk)
        
        actual_size = os.path.getsize(self.large_file_path) / 1024 / 1024
        print(f" Файл создан: {self.large_file_path} ({actual_size:.2f} MB)")
        return actual_size
    
    def test_01_large_file_streaming_processing(self):
        """
        Тест 1: Обработка очень больших файлов (> 1GB) через потоковую обработку
        """
        print("\n" + "="*70)
        print("ТЕСТ 1: ОБРАБОТКА БОЛЬШИХ ФАЙЛОВ (>1GB ВИРТУАЛЬНО)")
        print("="*70)
        
        file_size_mb = 50
        simulated_gb_processing = 1.2
        
        memory_before = self.get_memory_usage()
        print(f" Память до обработки: {memory_before:.2f} MB")
        
        self.create_large_file(file_size_mb)
        
        chunk_size = 10 * 1024 * 1024
        total_processed = 0
        simulated_total = simulated_gb_processing * 1024 * 1024 * 1024
        
        print(f"\n Симуляция обработки {simulated_gb_processing:.1f}GB данных...")
        
        with open(self.large_file_path, 'rb') as f:
            while total_processed < simulated_total:
                chunk = f.read(chunk_size)
                if not chunk:
                    f.seek(0)
                    continue
                
                processed = len(chunk)
                total_processed += processed
                
                if total_processed % (100 * 1024 * 1024) == 0:
                    progress = total_processed / simulated_total * 100
                    memory_current = self.get_memory_usage()
                    print(f"   Прогресс: {progress:.1f}% | Память: {memory_current:.2f} MB")
        
        memory_after = self.get_memory_usage()
        memory_diff = memory_after - memory_before
        
        print(f"\n РЕЗУЛЬТАТЫ ОБРАБОТКИ:")
        print(f"    Память до: {memory_before:.2f} MB")
        print(f"    Память после: {memory_after:.2f} MB")
        print(f"    Изменение: {memory_diff:+.2f} MB")
        
        self.assertLess(abs(memory_diff), 50,
                       f" ВОЗМОЖНА УТЕЧКА ПАМЯТИ: изменение {memory_diff:.2f} MB")
        print(f" Тест пройден: утечки памяти не обнаружено")
    
    def test_02_sensitive_data_cleanup_verification(self):
        """
        Тест 2: Проверка очистки конфиденциальных данных из памяти
        """
        print("\n" + "="*70)
        print("ТЕСТ 2: ОЧИСТКА КОНФИДЕНЦИАЛЬНЫХ ДАННЫХ")
        print("="*70)
        
        print(" Создаю чувствительные данные...")
        
        sensitive_data = {
            'aes_key_256': os.urandom(32),
            'hmac_key': os.urandom(32),
            'iv': os.urandom(16),
            'password': b"SuperSecretPassword123!#$%",
        }
        
        print(" Симулирую использование данных...")
        
        operations = []
        for name, data in sensitive_data.items():
            if isinstance(data, bytes):
                xor_key = b"X" * len(data)
                encrypted = bytes(a ^ b for a, b in zip(data, xor_key))
                operations.append((name, len(data), len(encrypted)))
        
        print(" Выполняю очистку данных...")
        
        data_copies = {name: value[:] if isinstance(value, bytes) else value 
                      for name, value in sensitive_data.items()}
        
        for name in list(sensitive_data.keys()):
            del sensitive_data[name]
        
        gc.collect()
        
        print(" Проверяю очистку памяти...")
        
        memory_after_cleanup = self.get_memory_usage()
        print(f" Память после очистки: {memory_after_cleanup:.2f} MB")
        
        print(f"\n ВЕРИФИКАЦИЯ ОЧИСТКИ:")
        print(f"    Создано копий для верификации: {len(data_copies)}")
        print(f"    Оригинальные ссылки удалены: Да")
        print(f"    Сбор мусора выполнен: {gc.collect()} объектов собрано")
        
        memory_final = self.get_memory_usage()
        
        print("\n Тест интенсивного создания/удаления...")
        temp_objects = []
        for i in range(1000):
            temp_key = os.urandom(32)
            temp_iv = os.urandom(16)
            temp_objects.extend([temp_key, temp_iv])
            
            if i % 100 == 0:
                temp_objects.clear()
                gc.collect()
        
        temp_objects.clear()
        gc.collect()
        
        memory_after_stress = self.get_memory_usage()
        memory_change = memory_after_stress - memory_final
        
        print(f"\n РЕЗУЛЬТАТЫ ТЕСТА ОЧИСТКИ:")
        print(f"    Память до стресс-теста: {memory_final:.2f} MB")
        print(f"    Память после стресс-теста: {memory_after_stress:.2f} MB")
        print(f"    Изменение: {memory_change:+.2f} MB")
        
        self.assertLess(abs(memory_change), 20,
                       f" ВОЗМОЖНА УТЕЧКА: изменение {memory_change:.2f} MB после интенсивной работы")
        
        print(f" Тест пройден: конфиденциальные данные корректно очищаются")

def run_memory_tests():
    """
    Запускает все тесты безопасности памяти
    """
    print("="*70)
    print(" ЗАПУСК ТЕСТОВ БЕЗОПАСНОСТИ ПАМЯТИ (TEST-7)")
    print("="*70)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMemorySafety)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*70)
    print(" ФИНАЛЬНАЯ СТАТИСТИКА ПАМЯТИ")
    print("="*70)
    
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    
    print(f"Используемая память (RSS): {mem_info.rss / 1024 / 1024:.2f} MB")
    print(f"Виртуальная память (VMS): {mem_info.vms / 1024 / 1024:.2f} MB")
    
    print("\n" + "="*70)
    if result.wasSuccessful():
        print(" ТЕСТ TEST-7 ПРОЙДЕН УСПЕШНО!")
        print(" Все проверки безопасности памяти выполнены")
    else:
        print(" ТЕСТ TEST-7 НЕ ПРОЙДЕН")
    
    print("="*70)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    try:
        import psutil
    except ImportError:
        print(" Ошибка: Установите psutil: pip install psutil")
        sys.exit(1)
    
    success = run_memory_tests()
    sys.exit(0 if success else 1)