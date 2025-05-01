const path = require('path');

module.exports = {
    // Disable source map loading for the entities package
    module: {
        rules: [
            {
                test: /node_modules\/entities\/.*\.js$/,
                use: [
                    {
                        loader: 'source-map-loader',
                        options: {
                            filterSourceMappingUrl: (url, resourcePath) => {
                                // Completely ignore source maps for entities package
                                if (resourcePath.includes('node_modules/entities/')) {
                                    return false;
                                }
                                return true;
                            }
                        }
                    }
                ],
                enforce: 'pre'
            }
        ]
    }
};
