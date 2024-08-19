import React from 'react';
import './Info.css';

// Import images
import brainImage from '../images/braincancer_info.jpg';
import kidneyImage from '../images/kidneycancer_info.jpg';
import breastImage from '../images/breastcancer_info.jpg';
import oralImage from '../images/oralcancer_info.jpg';

const cancerInfo = [
  {
    image: brainImage,
    title: 'Brain Cancer',
    description: `Brain cancer encompasses various types of tumors including gliomas (from glial cells), meningiomas (in the protective membranes around the brain), medulloblastomas (fast-growing tumors in the cerebellum), schwannomas (affecting balance and hearing nerves), pituitary tumors (affecting hormone production), and craniopharyngiomas (rare tumors near the pituitary gland).`
  },
  {
    image: kidneyImage,
    title: 'Kidney Cancer',
    description: `Kidney cancer includes renal cell carcinoma (RCC), the most common type, transitional cell carcinoma (TCC) affecting the renal pelvis, Wilms' tumor primarily in children, renal sarcoma from kidney connective tissues, and benign tumors like oncocytomas and angiomyolipomas which may still require treatment.`
  },
  {
    image: breastImage,
    title: 'Breast Cancer',
    description: `Breast cancer types include ductal carcinoma in situ (DCIS) which is non-invasive, invasive ductal carcinoma (IDC) starting in ducts and spreading, invasive lobular carcinoma (ILC) from milk-producing lobules, triple-negative breast cancer lacking estrogen, progesterone, and HER2 receptors, HER2-positive breast cancer with high HER2 levels, inflammatory breast cancer causing redness and swelling, Paget’s disease affecting the nipple, and phyllodes tumors in connective tissue.`
  },
  {
    image: oralImage,
    title: 'Oral Cancer',
    description: `Oral cancer types include squamous cell carcinoma (SCC), which is common and originates from squamous cells in the mouth and throat, verrucous carcinoma which is rare and slow-growing, minor salivary gland carcinomas like adenoid cystic carcinoma, mucosal melanoma occurring in mouth mucous membranes, and basal cell carcinoma (BCC) which can also appear in the oral cavity, particularly on the lips.`
  }
];

function Info() {
  return (
    <section id="info" className="info-section">
      {cancerInfo.map((item, index) => (
        <div
          key={index}
          className={`info-item ${index % 2 === 0 ? 'left' : 'right'} animate-item`}
          style={{ animationDelay: `${index * 0.3}s` }}
        >
          <img src={item.image} alt={item.title} className="info-image" />
          <div className="info-text">
            <h2 className="info-title">{item.title}</h2>
            <p className="info-description">{item.description}</p>
          </div>
        </div>
      ))}
    </section>
  );
}

export default Info;
