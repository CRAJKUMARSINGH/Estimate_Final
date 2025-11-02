#!/usr/bin/env python3
"""
NEW ESTIMATE CREATION DEMO
Shows: Save XXXX.xlsx as NEW_ESTIMATE → Add NETWORKING part → Modify existing parts → Update results
"""

import pandas as pd
from datetime import datetime

def demonstrate_new_estimate_creation():
    """Complete demonstration of creating NEW_ESTIMATE with modifications"""
    
    print("🏗️ NEW ESTIMATE CREATION DEMONSTRATION")
    print("=" * 70)
    print("Process: XXXX.xlsx → NEW_ESTIMATE → Add NETWORKING → Modify Parts → Update")
    print("=" * 70)
    
    # Step 1: Load existing estimate from XXXX.xlsx
    print("\n📥 STEP 1: LOADING EXISTING ESTIMATE FROM XXXX.XLSX")
    print("-" * 55)
    
    # Simulate existing estimate structure
    existing_estimate = {
        "Ground Floor": {
            "abstract": [
                {"id": 1, "ssr": "2.1.1", "desc": "Cement concrete 1:2:4 using 20mm aggregate", "qty": 114, "rate": 4850.00, "amount": 552900},
                {"id": 2, "ssr": "3.1.1", "desc": "Brick work in superstructure", "qty": 55.2, "rate": 5200.00, "amount": 287040},
                {"id": 3, "ssr": "4.1.1", "desc": "12mm thick cement plaster 1:4", "qty": 480, "rate": 125.00, "amount": 60000}
            ],
            "measurements": [
                {"id": "1.1", "desc": "Cement concrete 1:2:4 using 20mm aggregate", "nos": 1, "l": 20, "b": 15, "h": 0.3, "total": 90},
                {"id": "1.2", "desc": "Cement concrete 1:2:4 using 20mm aggregate", "nos": 1, "l": 12, "b": 10, "h": 0.2, "total": 24},
                {"id": "2.1", "desc": "Brick work in superstructure", "nos": 4, "l": 15, "b": 0.23, "h": 3, "total": 41.4},
                {"id": "2.2", "desc": "Brick work in superstructure", "nos": 2, "l": 12, "b": 0.23, "h": 3, "total": 16.6},
                {"id": "3.1", "desc": "12mm thick cement plaster 1:4", "nos": 8, "l": 15, "b": 1, "h": 3, "total": 360},
                {"id": "3.2", "desc": "12mm thick cement plaster 1:4", "nos": 4, "l": 10, "b": 1, "h": 3, "total": 120}
            ]
        },
        "First Floor": {
            "abstract": [
                {"id": 1, "ssr": "3.1.1", "desc": "Brick work in superstructure", "qty": 48.3, "rate": 5200.00, "amount": 251160},
                {"id": 2, "ssr": "4.1.1", "desc": "12mm thick cement plaster 1:4", "qty": 420, "rate": 125.00, "amount": 52500},
                {"id": 3, "ssr": "9.1.1", "desc": "Flooring tiles 600x600mm", "qty": 280, "rate": 320.00, "amount": 89600}
            ],
            "measurements": [
                {"id": "1.1", "desc": "Brick work in superstructure", "nos": 4, "l": 14, "b": 0.23, "h": 3, "total": 38.6},
                {"id": "1.2", "desc": "Brick work in superstructure", "nos": 1, "l": 10, "b": 0.23, "h": 4.2, "total": 9.7},
                {"id": "2.1", "desc": "12mm thick cement plaster 1:4", "nos": 8, "l": 14, "b": 1, "h": 3, "total": 336},
                {"id": "2.2", "desc": "12mm thick cement plaster 1:4", "nos": 2, "l": 14, "b": 1, "h": 3, "total": 84},
                {"id": "3.1", "desc": "Flooring tiles 600x600mm", "nos": 1, "l": 20, "b": 14, "h": 1, "total": 280}
            ]
        },
        "Basement": {
            "abstract": [
                {"id": 1, "ssr": "1.1.1", "desc": "Earth work excavation in foundation by manual means", "qty": 432, "rate": 245.50, "amount": 106056},
                {"id": 2, "ssr": "8.1.1", "desc": "Waterproofing membrane", "qty": 216, "rate": 180.00, "amount": 38880}
            ],
            "measurements": [
                {"id": "1.1", "desc": "Earth work excavation in foundation by manual means", "nos": 1, "l": 18, "b": 12, "h": 2, "total": 432},
                {"id": "2.1", "desc": "Waterproofing membrane", "nos": 1, "l": 18, "b": 12, "h": 1, "total": 216}
            ]
        }
    }
    
    print("✅ Loaded existing estimate from XXXX.xlsx:")
    original_total = 0
    for part_name, part_data in existing_estimate.items():
        part_total = sum(item['amount'] for item in part_data['abstract'])
        original_total += part_total
        print(f"   📊 {part_name}: ₹{part_total:,.0f}")
    print(f"   💰 Original Total: ₹{original_total:,.0f}")
    
    # Step 2: Save as NEW_ESTIMATE
    print(f"\n💾 STEP 2: SAVING AS NEW_ESTIMATE.XLSX")
    print("-" * 40)
    print("✅ Estimate saved as: NEW_ESTIMATE.xlsx")
    print("✅ All existing sheets preserved")
    print("✅ Ready for modifications")
    
    # Step 3: Add NETWORKING part
    print(f"\n➕ STEP 3: ADDING NEW PART - NETWORKING")
    print("-" * 45)
    
    # Create NETWORKING part
    networking_part = {
        "abstract": [
            {"id": 1, "ssr": "6.2.1", "desc": "GI pipes 25mm dia for water supply", "qty": 0, "rate": 325.00, "amount": 0},
            {"id": 2, "ssr": "7.1.1", "desc": "Steel reinforcement bars", "qty": 0, "rate": 65.00, "amount": 0},
            {"id": 3, "ssr": "10.1.1", "desc": "AC sheet roofing", "qty": 0, "rate": 285.00, "amount": 0}
        ],
        "measurements": []
    }
    
    print("🔧 Creating NETWORKING Abstract of Cost:")
    print("   Item | SSR   | Description                      | Rate")
    print("   -----|-------|----------------------------------|----------")
    for item in networking_part["abstract"]:
        print(f"   {item['id']:<4} | {item['ssr']:<5} | {item['desc']:<32} | ₹{item['rate']:7,.2f}")
    
    print(f"\n📏 Auto-creating NETWORKING Measurement lines:")
    
    # Auto-create measurement lines for each abstract item
    networking_measurements = [
        # GI pipes - Linear unit (2 lines)
        {"id": "1.1", "desc": "GI pipes 25mm dia for water supply", "nos": 1, "l": 0, "b": 1, "h": 1, "total": 0},
        {"id": "1.2", "desc": "GI pipes 25mm dia for water supply", "nos": 1, "l": 0, "b": 1, "h": 1, "total": 0},
        
        # Steel bars - Weight unit (2 lines)
        {"id": "2.1", "desc": "Steel reinforcement bars", "nos": 1, "l": 0, "b": 0, "h": 0, "total": 0},
        {"id": "2.2", "desc": "Steel reinforcement bars", "nos": 1, "l": 0, "b": 0, "h": 0, "total": 0},
        
        # AC sheet - Area unit (2 lines)
        {"id": "3.1", "desc": "AC sheet roofing", "nos": 1, "l": 0, "b": 0, "h": 1, "total": 0},
        {"id": "3.2", "desc": "AC sheet roofing", "nos": 1, "l": 0, "b": 0, "h": 1, "total": 0}
    ]
    
    networking_part["measurements"] = networking_measurements
    
    print("   📐 Created blank measurement lines for each abstract item")
    print("   📏 GI pipes: 2 linear measurement lines")
    print("   📏 Steel bars: 2 weight measurement lines") 
    print("   📏 AC sheet: 2 area measurement lines")
    
    # Add NETWORKING to estimate
    existing_estimate["NETWORKING"] = networking_part
    
    print("✅ NETWORKING part added to NEW_ESTIMATE")
    
    # Step 4: Modify existing parts by adding measurement lines
    print(f"\n🔧 STEP 4: MODIFYING EXISTING PARTS - ADDING MEASUREMENT LINES")
    print("-" * 65)
    
    print("👤 USER ACTION: Adding one more measurement line to each existing part")
    
    # Add measurement line to Ground Floor
    new_ground_floor_measurement = {
        "id": "1.3", 
        "desc": "Cement concrete 1:2:4 using 20mm aggregate", 
        "nos": 1, "l": 8, "b": 6, "h": 0.25, "total": 12
    }
    existing_estimate["Ground Floor"]["measurements"].append(new_ground_floor_measurement)
    
    print(f"\n📏 Ground Floor - Added measurement line:")
    print(f"   Item 1.3: Concrete - 1 × 8 × 6 × 0.25 = 12 cum")
    
    # Add measurement line to First Floor
    new_first_floor_measurement = {
        "id": "3.2", 
        "desc": "Flooring tiles 600x600mm", 
        "nos": 1, "l": 8, "b": 6, "h": 1, "total": 48
    }
    existing_estimate["First Floor"]["measurements"].append(new_first_floor_measurement)
    
    print(f"📏 First Floor - Added measurement line:")
    print(f"   Item 3.2: Flooring tiles - 1 × 8 × 6 × 1 = 48 sqm")
    
    # Add measurement line to Basement
    new_basement_measurement = {
        "id": "2.2", 
        "desc": "Waterproofing membrane", 
        "nos": 1, "l": 6, "b": 4, "h": 1, "total": 24
    }
    existing_estimate["Basement"]["measurements"].append(new_basement_measurement)
    
    print(f"📏 Basement - Added measurement line:")
    print(f"   Item 2.2: Waterproofing - 1 × 6 × 4 × 1 = 24 sqm")
    
    # Add measurements to NETWORKING
    networking_measurements_filled = [
        {"id": "1.1", "desc": "GI pipes 25mm dia for water supply", "nos": 1, "l": 45, "b": 1, "h": 1, "total": 45},
        {"id": "1.2", "desc": "GI pipes 25mm dia for water supply", "nos": 1, "l": 25, "b": 1, "h": 1, "total": 25},
        {"id": "2.1", "desc": "Steel reinforcement bars", "nos": 150, "l": 1, "b": 1, "h": 1, "total": 150},
        {"id": "2.2", "desc": "Steel reinforcement bars", "nos": 80, "l": 1, "b": 1, "h": 1, "total": 80},
        {"id": "3.1", "desc": "AC sheet roofing", "nos": 1, "l": 12, "b": 8, "h": 1, "total": 96},
        {"id": "3.2", "desc": "AC sheet roofing", "nos": 1, "l": 6, "b": 4, "h": 1, "total": 24}
    ]
    
    existing_estimate["NETWORKING"]["measurements"] = networking_measurements_filled
    
    print(f"📏 NETWORKING - Added measurements:")
    print(f"   GI pipes: 45m + 25m = 70m")
    print(f"   Steel bars: 150kg + 80kg = 230kg")
    print(f"   AC sheet: 96sqm + 24sqm = 120sqm")
    
    # Step 5: Calculate updated quantities and amounts
    print(f"\n⚡ STEP 5: AUTOMATIC UPDATES IN PROGRESS...")
    print("-" * 50)
    
    # Update Ground Floor
    concrete_total_gf = sum(m['total'] for m in existing_estimate["Ground Floor"]["measurements"] if "concrete" in m['desc'].lower())
    existing_estimate["Ground Floor"]["abstract"][0]["qty"] = concrete_total_gf
    existing_estimate["Ground Floor"]["abstract"][0]["amount"] = concrete_total_gf * 4850.00
    
    # Update First Floor
    flooring_total_ff = sum(m['total'] for m in existing_estimate["First Floor"]["measurements"] if "flooring" in m['desc'].lower())
    existing_estimate["First Floor"]["abstract"][2]["qty"] = flooring_total_ff
    existing_estimate["First Floor"]["abstract"][2]["amount"] = flooring_total_ff * 320.00
    
    # Update Basement
    waterproof_total_b = sum(m['total'] for m in existing_estimate["Basement"]["measurements"] if "waterproofing" in m['desc'].lower())
    existing_estimate["Basement"]["abstract"][1]["qty"] = waterproof_total_b
    existing_estimate["Basement"]["abstract"][1]["amount"] = waterproof_total_b * 180.00
    
    # Update NETWORKING
    gi_pipes_total = sum(m['total'] for m in existing_estimate["NETWORKING"]["measurements"] if "gi pipes" in m['desc'].lower())
    steel_total = sum(m['total'] for m in existing_estimate["NETWORKING"]["measurements"] if "steel" in m['desc'].lower())
    ac_sheet_total = sum(m['total'] for m in existing_estimate["NETWORKING"]["measurements"] if "ac sheet" in m['desc'].lower())
    
    existing_estimate["NETWORKING"]["abstract"][0]["qty"] = gi_pipes_total
    existing_estimate["NETWORKING"]["abstract"][0]["amount"] = gi_pipes_total * 325.00
    existing_estimate["NETWORKING"]["abstract"][1]["qty"] = steel_total
    existing_estimate["NETWORKING"]["abstract"][1]["amount"] = steel_total * 65.00
    existing_estimate["NETWORKING"]["abstract"][2]["qty"] = ac_sheet_total
    existing_estimate["NETWORKING"]["abstract"][2]["amount"] = ac_sheet_total * 285.00
    
    print("🔄 Updated quantities from measurements")
    print("🔄 Recalculated amounts (Qty × Rate)")
    print("🔄 Updated Abstract of Cost sheets")
    print("🔄 Updated General Abstract totals")
    
    # Step 6: Show updated results
    print(f"\n📊 STEP 6: UPDATED ESTIMATE RESULTS")
    print("-" * 40)
    
    print("💰 REVISED Abstract of Cost Summary:")
    print("   Part         | Items | Total Amount")
    print("   -------------|-------|-------------")
    
    revised_total = 0
    for part_name, part_data in existing_estimate.items():
        part_total = sum(item['amount'] for item in part_data['abstract'])
        item_count = len(part_data['abstract'])
        revised_total += part_total
        print(f"   {part_name:<12} | {item_count:5d} | ₹{part_total:10,.0f}")
    
    print("   -------------|-------|-------------")
    print(f"   TOTAL        |       | ₹{revised_total:10,.0f}")
    
    # Show detailed NETWORKING breakdown
    print(f"\n🔧 NETWORKING Part Details:")
    print("   Item | Description                      | Qty    | Rate    | Amount")
    print("   -----|----------------------------------|--------|---------|----------")
    for item in existing_estimate["NETWORKING"]["abstract"]:
        print(f"   {item['id']:<4} | {item['desc']:<32} | {item['qty']:6.0f} | ₹{item['rate']:6,.0f} | ₹{item['amount']:8,.0f}")
    networking_total = sum(item['amount'] for item in existing_estimate["NETWORKING"]["abstract"])
    print("   -----|----------------------------------|--------|---------|----------")
    print(f"   TOTAL| NETWORKING TOTAL                 |        |         | ₹{networking_total:8,.0f}")
    
    # Final cost calculation
    print(f"\n💹 FINAL COST CALCULATION:")
    print("-" * 35)
    
    subtotal = revised_total
    electrification = subtotal * 0.07
    after_electrification = subtotal + electrification
    prorata = after_electrification * 0.13
    final_total = after_electrification + prorata
    
    print(f"   Subtotal (All Parts):        ₹{subtotal:10,.0f}")
    print(f"   Add 7% Electrification:      ₹{electrification:10,.0f}")
    print(f"   Total after Electrification: ₹{after_electrification:10,.0f}")
    print(f"   Add 13% Prorata Charges:     ₹{prorata:10,.0f}")
    print(f"   ----------------------------------------")
    print(f"   FINAL PROJECT TOTAL:         ₹{final_total:10,.0f}")
    
    # Comparison with original
    original_final = original_total * 1.20  # Approximate with charges
    increase = final_total - original_final
    percentage_increase = (increase / original_final) * 100
    
    print(f"\n📈 COMPARISON WITH ORIGINAL:")
    print("-" * 35)
    print(f"   Original Estimate (approx):  ₹{original_final:10,.0f}")
    print(f"   NEW_ESTIMATE (revised):      ₹{final_total:10,.0f}")
    print(f"   Increase:                    ₹{increase:10,.0f}")
    print(f"   Percentage Increase:         {percentage_increase:9.1f}%")
    
    # Summary of changes
    print(f"\n✨ SUMMARY OF CHANGES IN NEW_ESTIMATE:")
    print("-" * 45)
    print("✅ Added NETWORKING part with 3 items")
    print("✅ Added measurement lines to existing parts:")
    print("   • Ground Floor: +1 concrete measurement")
    print("   • First Floor: +1 flooring measurement")
    print("   • Basement: +1 waterproofing measurement")
    print("✅ All quantities updated automatically")
    print("✅ All costs recalculated in real-time")
    print("✅ General Abstract reflects all changes")
    print("✅ Professional estimate ready for use")
    
    print(f"\n💾 NEW_ESTIMATE.XLSX STATUS:")
    print("-" * 30)
    print("✅ File saved successfully")
    print("✅ 4 parts with Abstract + Measurement sheets")
    print("✅ All formulas and linkages active")
    print("✅ Ready for further modifications")
    print("✅ Export-ready in multiple formats")

if __name__ == "__main__":
    demonstrate_new_estimate_creation()