"""
Simple validation test for project setup
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 60)
print("INSTAGRAM AUTOMATION - PROJECT SETUP VALIDATION")
print("=" * 60)

try:
    print("\n[1/5] Testing imports...")
    from utils.logger import setup_logger, get_logger
    from utils.config import get_config
    from utils.validators import Validators
    from database.db_manager import DatabaseManager
    from PyQt5.QtWidgets import QApplication
    import instagrapi
    from apscheduler.schedulers.background import BackgroundScheduler
    print("✓ All critical modules imported successfully")
    
    print("\n[2/5] Testing configuration...")
    config = get_config()
    print(f"✓ Config initialized - Database: {config.database_path}")
    
    print("\n[3/5] Testing logger...")
    logger = setup_logger('test')
    logger.info("Test message")
    print("✓ Logger working")
    
    print("\n[4/5] Testing database...")
    db = DatabaseManager("data/test.db")
    account_id = db.add_account("test_user")
    account = db.get_account(account_id)
    os.remove("data/test.db")
    print(f"✓ Database working - Created and retrieved account '{account.username}'")
    
    print("\n[5/5] Testing validators...")
    valid, _ = Validators.validate_instagram_username("test_user")
    invalid, _ = Validators.validate_instagram_username("bad username!")
    assert valid and not invalid
    print("✓ Validators working correctly")
    
    print("\n" + "=" * 60)
    print("✓✓✓ ALL TESTS PASSED - PROJECT SETUP COMPLETE! ✓✓✓")
    print("=" * 60)
    print("\nYou can now run: python main.py")
    sys.exit(0)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 60)
    print("✗ SETUP VALIDATION FAILED")
    print("=" * 60)
    sys.exit(1)
