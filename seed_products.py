
import argparse
from decimal import Decimal
from uuid import uuid4

from src.connections.postgresql import SessionLocal
from src.models.product import Product
from src.models.vendor import Vendor


VENDOR_ID = 1
BATCH_SIZE = 5000


def seed_products(target_total: int):
    db = SessionLocal()

    try:
        vendor = (
            db.query(Vendor)
            .filter(Vendor.id == VENDOR_ID)
            .first()
        )

        if vendor is None:
            raise ValueError(
                f"Vendor with id {VENDOR_ID} does not exist."
            )

        current_count = db.query(Product).count()

        print(f"Current products: {current_count}")
        print(f"Target products: {target_total}")

        if current_count >= target_total:
            print("Target already reached. Nothing to insert.")
            return

        remaining = target_total - current_count

        print(f"Products to insert: {remaining}")

        inserted = 0

        while inserted < remaining:
            batch_count = min(
                BATCH_SIZE,
                remaining - inserted
            )

            products = []

            for _ in range(batch_count):
                unique_code = uuid4().hex[:12]

                product = Product(
                    name=f"Load Test Product {unique_code}",
                    description="Generated for performance testing",
                    price=Decimal("100000"),
                    stock=100,
                    vendor_id=VENDOR_ID,
                    is_active=True,
                )

                products.append(product)

            try:
                db.add_all(products)
                db.commit()

                inserted += batch_count

                print(
                    f"Inserted: {inserted}/{remaining}"
                )

            except Exception:
                db.rollback()
                raise

        final_count = db.query(Product).count()

        print("--------------------------------")
        print("Seeding completed successfully.")
        print(f"Final product count: {final_count}")
        print("--------------------------------")

    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--target",
        type=int,
        required=True,
        help="Total number of products required"
    )

    args = parser.parse_args()

    seed_products(args.target)
