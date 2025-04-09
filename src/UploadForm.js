import React, { useState } from 'react';

function UploadDatasetForm() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [datasetName, setDatasetName] = useState('');
  const [datasetDescription, setDatasetDescription] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleNameChange = (event) => {
    setDatasetName(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDatasetDescription(event.target.value);
  };

  const handleSubmit = async (event) => {
        event.preventDefault();
    
        if (!selectedFile) {
          alert('Por favor, selecione um arquivo CSV.');
          return;
        }
    
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('nome', datasetName);
        formData.append('descricao', datasetDescription);
    
        try {
          const token = localStorage.getItem('seuTokenJWT'); // Substitua 'seuTokenJWT' pela chave onde você armazena o token
          const response = await fetch('/api/v1/upload/', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`, // Inclua o token se a sua API exigir
            },
            body: formData,
          });
    
          if (response.ok) {
            const data = await response.json();
            alert(data.message); // Exibe a mensagem de sucesso do backend
            // Opcional: Limpar o formulário após o sucesso
            setSelectedFile(null);
            setDatasetName('');
            setDatasetDescription('');
          } else {
            const errorData = await response.json();
            alert(`Erro no upload: ${errorData.detail || 'Erro desconhecido'}`);
          }
        } catch (error) {
          console.error('Erro ao enviar o arquivo:', error);
          alert('Ocorreu um erro ao enviar o arquivo.');
        }
       };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="file">
          Selecionar Arquivo CSV
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="file"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
          Nome do Dataset
        </label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="name"
          type="text"
          placeholder="Nome do seu dataset"
          value={datasetName}
          onChange={handleNameChange}
          required
        />
      </div>
      <div className="mb-6">
        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="description">
          Descrição do Dataset
        </label>
        <textarea
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="description"
          placeholder="Breve descrição do seu dataset"
          value={datasetDescription}
          onChange={handleDescriptionChange}
          rows="4"
        />
      </div>
      <div className="flex items-center justify-between">
        <button
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="submit"
        >
          Enviar Dataset
        </button>
      </div>
    </form>
  );
}

export default UploadDatasetForm;