import React, { useState } from 'react';
import axios from "axios";
import './Test.css';

function ImageUpload() {
  const [image, setImage] = useState([]);
  const [responseMsg, setResponseMsg] = useState({
    status: "",
    message: "",
    error: "",
  });

  const [prediction, setPrediction] = useState("Nothing");
  const [loading, setLoading] = useState(false); // New loading state

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file && fileValidate(file)) {
      setImage([file]);
    } else {
      setImage([]);
    }
  };

  const submitHandler = (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append("files[]", image[0]);

    axios.post("/upload", data)
      .then((response) => {
        if (response.status === 201) {
          setResponseMsg({
            status: response.data.status,
            message: response.data.message,
            error: "",
          });
          setTimeout(() => {
            setImage([]);
            setResponseMsg({
              status: "",
              message: "",
              error: "",
            });
          }, 100000);

          document.querySelector("#imageForm").reset();
        }
        alert("Successfully Uploaded.");
      })
      .catch((error) => {
        if (error.response && error.response.status === 401) {
          alert("Invalid credentials.");
        }
      });
  };

  const fileValidate = (file) => {
    if (
      file.type === "image/png" ||
      file.type === "image/jpg" ||
      file.type === "image/jpeg"
    ) {
      setResponseMsg((prevState) => ({
        ...prevState,
        error: "",
      }));
      return true;
    } else {
      setResponseMsg((prevState) => ({
        ...prevState,
        error: "File type allowed only jpg, png, jpeg",
      }));
      return false;
    }
  };

  const fetchPrediction = () => {
    setLoading(true); // Set loading to true when fetching starts
    axios.get('/analyze')
      .then((response) => {
        const predictedLabel = response.data.predicted_label;
        setPrediction(predictedLabel);
        setLoading(false); // Set loading to false once the prediction is fetched
      })
      .catch((error) => {
        console.log(error);
        setLoading(false); // In case of an error, also set loading to false
      });
  };

  const clearFiles = () => {
    setImage([]);
    setResponseMsg({
      status: "",
      message: "",
      error: "",
    });
    document.querySelector("#imageForm").reset();
    
    // Set the label to be nothing
    const predictedLabel = "Nothing";
    setPrediction(predictedLabel);

    axios.get('/delete')
    .then((response) => {
      if (response.status === 201) {
        setResponseMsg({
          status: response.data.status,
          message: response.data.message,
          error: "",
        });
        setTimeout(() => {
          setImage([]);
          setResponseMsg({
            status: "",
            message: "",
            error: "",
          });
        }, 100000);
      }
      alert("Successfully Deleted.");
    })
    .catch((error) => {
      if (error.response && error.response.status === 401) {
        alert("Invalid credentials.");
      }
    });
  };

  return (
    <div className="container py-5">
      {/* Overlay for loading spinner */}
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
        </div>
      )}

      <div className={`row ${loading ? 'disabled' : ''}`}>
        <div className="col-lg-12">
          <form onSubmit={submitHandler} encType="multipart/form-data" id="imageForm">
            <div className="card shadow">
              {responseMsg.status === "success" ? (
                <div className="alert alert-success">
                  {responseMsg.message}
                </div>
              ) : responseMsg.status === "failed" ? (
                <div className="alert alert-danger">
                  {responseMsg.message}
                </div>
              ) : null}
              <div className="card-header">
                <h4 className="card-title fw-bold">
                  Concerned about your health?<br></br>Upload a picture of a medical scan to begin.
                </h4>
                <h3>
                  (One picture at a time)
                </h3>
              </div>

              <div className="card-body">
                <div className="form-group py-2">
                  <label htmlFor="images">Image Upload: </label>
                  <input
                    type="file"
                    name="image"
                    onChange={handleChange}
                    className="form-control"
                  />
                  <span className="text-danger">
                    {responseMsg.error}
                  </span>
                </div>
              </div>
              <div className="card-footer button-group">
                <button type="submit" className="btn btn-success">
                  Upload
                </button>
                <button
                  type = "button"
                  id="remove"
                  className="delete"
                  onClick={clearFiles}
                >
                  Clear
                </button>
              </div>
            </div>
          </form>
          <div>
            <button id="submit" className="button" onClick={fetchPrediction} disabled={loading}>
              Analyze
            </button>
          </div>
          <div>
            <h1>Your diagnosis is: {prediction}</h1>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ImageUpload;