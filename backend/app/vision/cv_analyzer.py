from PIL import Image, ImageFilter, ImageStat
import numpy as np

def analyze_material_image(image_path: str):
    """Analyze real visual characteristics of material photos."""
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    # 1. Color and material hint
    stat = ImageStat.Stat(img)
    r_mean, g_mean, b_mean = stat.mean[:3]
    
    # Check red/terracotta dominance (brick/tile)
    is_reddish = r_mean > 1.2 * max(g_mean, b_mean)
    is_grey = abs(r_mean - g_mean) < 15 and abs(g_mean - b_mean) < 15
    
    # 2. Edge / crack / fracture detection
    gray = img.convert('L')
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_stat = ImageStat.Stat(edges)
    edge_density = edge_stat.mean[0] # Higher = more rough, cracked, or fractured
    
    # 3. Contour / Fragmentation Analysis
    # Threshold to find foreground object vs background
    arr = np.array(gray)
    # Check background color from corners
    corners = [arr[0, 0], arr[0, -1], arr[-1, 0], arr[-1, -1]]
    bg_val = np.median(corners)
    
    # Contrast with background
    diff = np.abs(arr.astype(np.int32) - bg_val)
    mask = diff > 30 # foreground
    
    # Check for fragmentation/gaps in foreground
    # A solid brick has continuous foreground; a broken one has gaps/fissures
    vertical_profile = np.sum(mask, axis=0)
    horizontal_profile = np.sum(mask, axis=1)
    
    # Count significant drops inside the object region (fissures/breaks)
    non_zero_cols = np.where(vertical_profile > (height * 0.05))[0]
    has_deep_split = False
    split_count = 0
    
    if len(non_zero_cols) > 20:
        col_start, col_end = non_zero_cols[0], non_zero_cols[-1]
        interior = vertical_profile[col_start:col_end]
        min_in_interior = np.min(interior)
        max_in_interior = np.max(interior)
        if max_in_interior > 0 and (min_in_interior / max_in_interior) < 0.35:
            has_deep_split = True
            split_count += 1

    # Heuristic condition grading
    if has_deep_split or edge_density > 45:
        condition_estimate = "poor"
        defects = ["severe structural fracture/breakage", "split into multiple fragments", "heavy material loss"]
        suggested_reuse = "recycle"
        integrity_score = 25
    elif edge_density > 25:
        condition_estimate = "fair"
        defects = ["surface cracking", "chipped edges", "moderate weathering"]
        suggested_reuse = "verify_then_reuse"
        integrity_score = 60
    elif edge_density > 15:
        condition_estimate = "good"
        defects = ["minor edge wear", "minor surface roughness"]
        suggested_reuse = "reuse"
        integrity_score = 80
    else:
        condition_estimate = "excellent"
        defects = ["clean edges", "intact surface"]
        suggested_reuse = "reuse"
        integrity_score = 95
        
    return {
        "width": width,
        "height": height,
        "has_deep_split": has_deep_split,
        "edge_density": round(edge_density, 2),
        "condition_estimate": condition_estimate,
        "detected_defects": defects,
        "suggested_reuse": suggested_reuse,
        "integrity_score": integrity_score,
        "is_reddish": is_reddish,
        "is_grey": is_grey
    }

if __name__ == "__main__":
    import sys
    test_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\lenovo\.gemini\antigravity\brain\db35918a-fa81-40a7-8c68-7717e5e6c206\media__1789104724446.jpg"
    res = analyze_material_image(test_path)
    print("CV Analysis Result:", res)
