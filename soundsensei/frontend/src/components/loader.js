import React, { useState } from 'react';

const LoadingModal = ({showModal}) => {
//   const [showModal, setShowModal] = useState(modalOpen);

//   const closeModal = () => {
//     setShowModal(false);
//   };

  return (
    <div>
      {showModal && (
        <div style={styles.modal}>
          <div style={styles.modalContent} className='loader-class'>
            <h1 style={{padding: "5px", fontSize: '2rem', fontFamily: 'Lexend Peta'}}>Loading...</h1>
            <div style={styles.loader}></div>
            {/* <button onClick={closeModal}>Close</button> */}
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  modal: {
    position: 'fixed',
    left: '0',
    top: '0',
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: '100',
    fontFamily: 'Lexenda Peta'
  },
  modalContent: {
    display: 'flex',
    flexDirection: 'column',
    justifyItems: 'center',
    alignContent: 'center',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'transparent',
    padding: '20px',
    borderRadius: '5px',
    textAlign: 'center',
    fontFamily: 'Lexenda Peta'
  },
  loader: {
    border: '16px solid #f3f3f3',
    borderTop: '16px solid #3498db',
    borderRadius: '50%',
    width: '100px',
    height: '100px',
    animation: 'spin 2s linear infinite',
  },
};

export default LoadingModal;