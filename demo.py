# EPI Demo Script
# This is a simple demonstration of EPI Recorder

print("=" * 50)
print("EPI RECORDER DEMONSTRATION")
print("=" * 50)

# Step 1: Basic calculation
print("\n📊 Step 1: Doing some calculations...")
result = 25 + 17
print(f"   25 + 17 = {result}")

# Step 2: Working with data
print("\n📝 Step 2: Creating some data...")
data = {
    "name": "EPI Demo",
    "version": "2.1.0",
    "status": "Recording in progress!"
}
print(f"   Created data: {data}")

# Step 3: Creating a file
print("\n📄 Step 3: Writing to a file...")
with open("demo_output.txt", "w") as f:
    f.write("This file was created during EPI recording!\n")
    f.write(f"Calculation result: {result}\n")
    f.write(f"Data: {data}\n")
print("   ✅ File 'demo_output.txt' created!")

# Step 4: Loop demonstration
print("\n🔄 Step 4: Processing items...")
items = ["Alpha", "Beta", "Gamma"]
for i, item in enumerate(items, 1):
    print(f"   Processing item {i}: {item}")

print("\n" + "=" * 50)
print("✨ DEMONSTRATION COMPLETE!")
print("=" * 50)
print("\nEPI has recorded everything that just happened!")
print("Check the browser viewer to see the timeline.")
