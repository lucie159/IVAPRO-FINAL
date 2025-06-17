import cv2

# === Chemins vers les fichiers (à adapter selon ton projet) ===
template_path = "elonMusk.mp4_scene5_39.jpg"  # image du motif
frame_path = "d.png"  # image de la frame à tester

# === Chargement des images en niveaux de gris ===
template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
img = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)

# === Vérification du chargement ===
if template is None:
    print(f"[ERREUR] Template non trouvé à : {template_path}")
elif img is None:
    print(f"[ERREUR] Frame non trouvée à : {frame_path}")
else:
    # === Matching (TM_CCOEFF_NORMED) ===
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print(f"Score de correspondance : {max_val:.4f}")
    print(f"Position de la correspondance : {max_loc}")

    # === Dessin du rectangle sur l'image ===
    h, w = template.shape
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    img_result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)  # pour dessiner en couleur
    cv2.rectangle(img_result, top_left, bottom_right, (0, 255, 0), 2)

    # === Affichage de l'image résultante ===
    cv2.imshow("Résultat du matching", img_result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
