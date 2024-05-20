function calculateStringSimilarity(str1, str2) {
    const len1 = str1.length;
    const len2 = str2.length;

    // Create a 2D array to store the distances
    const distances = [];
    for (let i = 0; i <= len1; i++) {
        distances[i] = [];
        distances[i][0] = i;
    }
    for (let j = 0; j <= len2; j++) {
        distances[0][j] = j;
    }

    // Calculate Levenshtein distance
    for (let j = 1; j <= len2; j++) {
        for (let i = 1; i <= len1; i++) {
            if (str1[i - 1] === str2[j - 1]) {
                distances[i][j] = distances[i - 1][j - 1];
            } else {
                distances[i][j] = Math.min(
                    distances[i - 1][j] + 1, // Deletion
                    distances[i][j - 1] + 1, // Insertion
                    distances[i - 1][j - 1] + 1 // Substitution
                );
            }
        }
    }

    // The similarity score is inversely proportional to the Levenshtein distance
    // Here, we use a simple transformation: similarity = 1 / (1 + distance)
    const similarity = 1 / (1 + distances[len1][len2]);
    return similarity;
}



