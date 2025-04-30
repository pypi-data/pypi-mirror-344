#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Base directory for entities package
const entitiesDir = path.resolve('./node_modules/entities/lib/esm');

// Function to recursively find all .js files
function findJsFiles(dir, fileList = []) {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory()) {
            findJsFiles(filePath, fileList);
        } else if (file.endsWith('.js')) {
            fileList.push(filePath);
        }
    });

    return fileList;
}

// Function to fix source map URLs in a file
function fixSourceMapUrl(filePath) {
    console.log(`Processing ${filePath}`);

    let content = fs.readFileSync(filePath, 'utf8');

    // Check if the file has a sourceMappingURL comment
    const sourceMappingUrlRegex = /\/\/# sourceMappingURL=(.+)$/m;
    const match = content.match(sourceMappingUrlRegex);

    if (match) {
        const sourceMapUrl = match[1];
        console.log(`  Found sourceMappingURL: ${sourceMapUrl}`);

        // Remove the sourceMappingURL comment
        content = content.replace(sourceMappingUrlRegex, '');

        // Write the modified content back to the file
        fs.writeFileSync(filePath, content);
        console.log(`  Removed sourceMappingURL from ${filePath}`);
    }
}

// Main function
function main() {
    console.log('Fixing source map URLs in entities package...');

    try {
        // Find all .js files in the entities package
        const jsFiles = findJsFiles(entitiesDir);

        // Fix source map URLs in each file
        jsFiles.forEach(fixSourceMapUrl);

        console.log('Done!');
    } catch (error) {
        console.error('Error:', error);
    }
}

main();
