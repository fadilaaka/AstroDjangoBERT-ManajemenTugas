import React, { useEffect, useState } from "react";
import axios from "axios";

const ListTask = () => {
  const [data, setData] = useState([]);
  const [triggerState, setTriggerState] = useState(false);

  const deleteButton = (id) => {
    axios
      .delete(`http://127.0.0.1:8000/api/hapusdata/${id}`)
      .then((response) => {
        setTriggerState(true);
        console.log(response);
      })
      .catch((err) => console.log(err));
    setTriggerState(false);
  };

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/tugas")
      .then((response) => {
        console.log(response.data.data);
        setData(response.data.data);
      })
      .catch((err) => console.error(err));
  }, [triggerState]);

  return (
    <>
      <h1 className="font-bold text-xl mt-8 mb-5">Prioritas Rendah</h1>
      <div className="grid grid-cols-4 gap-5 items-stretch">
        {data &&
          data
            .filter((item) => item.prioritas === "rendah")
            .map((item, index) => (
              <div
                key={index}
                className="flex flex-col bg-white p-5 rounded-xl shadow-xl w-full"
              >
                <button
                  onClick={() => deleteButton(item.id)}
                  className="text-red-600 self-end"
                >
                  X
                </button>
                <h1 className="font-bold text-gray-900">{item.judul}</h1>
                <p className="font-normal text-gray-600">{item.deskripsi}</p>
                <span className="text-green-600">{item.prioritas}</span>
                <span className="text-red-500">{item.status}</span>
                <p className="text-blue-500">Deadline: {item.deadline}</p>
                <button className="bg-yellow-400 text-gray-800 rounded-xl hover:opacity-50 transition-all w-fit px-4 py-2 mt-8">
                  Edit Task
                </button>
              </div>
            ))}
      </div>
      <h1 className="font-bold text-xl mt-8 mb-5">Prioritas Sedang</h1>
      <div className="grid grid-cols-4 gap-5 items-stretch">
        {data &&
          data
            .filter((item) => item.prioritas === "sedang")
            .map((item, index) => (
              <div
                key={index}
                className="flex flex-col bg-white p-5 rounded-xl shadow-xl"
              >
                <button
                  onClick={() => deleteButton(item.id)}
                  className="text-red-600 self-end"
                >
                  X
                </button>
                <h1 className="font-bold text-gray-900">{item.judul}</h1>
                <p className="font-normal text-gray-600">{item.deskripsi}</p>
                <span className="text-green-600">{item.prioritas}</span>
                <span className="text-red-500">{item.status}</span>
                <p className="text-blue-500">Deadline: {item.deadline}</p>
                <button className="bg-yellow-400 text-gray-800 rounded-xl hover:opacity-50 transition-all w-fit px-4 py-2 mt-8">
                  Edit Task
                </button>
              </div>
            ))}
      </div>
      <h1 className="font-bold text-xl mt-8 mb-5">Prioritas Tinggi</h1>
      <div className="grid grid-cols-4 gap-5 items-stretch">
        {data &&
          data
            .filter((item) => item.prioritas === "tinggi")
            .map((item, index) => (
              <div
                key={index}
                className="flex flex-col bg-white p-5 rounded-xl shadow-xl"
              >
                <button
                  onClick={() => deleteButton(item.id)}
                  className="text-red-600 self-end"
                >
                  X
                </button>
                <h1 className="font-bold text-gray-900">{item.judul}</h1>
                <p className="font-normal text-gray-600">{item.deskripsi}</p>
                <span className="text-green-600">{item.prioritas}</span>
                <span className="text-red-500">{item.status}</span>
                <p className="text-blue-500">Deadline: {item.deadline}</p>
                <button className="bg-yellow-400 text-gray-800 rounded-xl hover:opacity-50 transition-all w-fit px-4 py-2 mt-8">
                  Edit Task
                </button>
              </div>
            ))}
      </div>
    </>
  );
};

export default ListTask;
