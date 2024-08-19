import React from 'react';

function ImageDisplay({ image }) {
    return (
        <div className="image-display-container">
            {image && (
                <>
                    <img src={image.base64} alt="Uploaded" className="uploaded-image" />
                    <div className="button-container">
                        <button className="analyze-button">Analyze</button>
                        <button className="info-button">Get More Info</button>
                    </div>
                </>
            )}
        </div>
    );
}

export default ImageDisplay;