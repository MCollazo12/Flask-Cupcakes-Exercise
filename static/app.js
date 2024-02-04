$(document).ready(function (e) {
  const BASE_URL = 'http://localhost:5000/api';
  const cupcake_form = document.getElementById('#cupcake-form');

  //Function to fetch cupcakes from API and display them on the index page
  function generateCupcakeHTML(cupcake) {
    return `
            <div data-id=${cupcake.id} class="col-md-3 mb-3" id="cupcake-container">
                <div class="card">
                    <img src="${cupcake.image}" class="card-img-top img-border" id="cupcake-img">
                    <div class="card-body">
                        <h5 class="card-title">${cupcake.flavor}</h5>
                        <p class="card-text">${cupcake.size} / ${cupcake.rating} star rating</p>
                        <button class="del-btn btn btn-warning">Delete</button>
                    </div>
                </div>
            </div>
            `;
  }

  async function listCupcakes() {
    const resp = await axios.get(`${BASE_URL}/cupcakes`).then(function (resp) {
      const cupcakes = resp.data.cupcakes;
      const cupcakeList = $('#cupcake-list');

      cupcakeList.empty();
      cupcakes.forEach(function (cupcake) {
        cupcakeList.append(generateCupcakeHTML(cupcake));
      });
    });
  }

  async function postNewCupcake(formData) {
    const resp = await axios.post('/api/cupcakes', formData);

    if (resp.data) {
      let new_cupcake = $(generateCupcakeHTML(resp.data.cupcake));
      $('#cupcake-list').append(new_cupcake);
      cupcake_form.reset();
    }
  }

  $('#cupcake-form').on('submit', async function (e) {
    e.preventDefault();

    let flavor = $('#flavor').val();
    let rating = selectedRatingId;
    let size = $('#size').val();
    let image = $('#image').val();

    const data = {
      flavor: flavor,
      rating: rating,
      size: size,
      image: image,
    };

    console.log(data);

    await postNewCupcake(data);
  });

  $('.btn-group').on('click', '.btn-secondary', function () {
    // Remove 'clicked' class from all buttons and replace with 'clicked
    $('.btn-secondary').removeClass('clicked');
    $(this).addClass('clicked');

    // Store the selected rating ID
    selectedRatingId = $(this).data('id');
  });

  $('#cupcake-list').on('click', '.del-btn', async function (e) {
    e.preventDefault();

    // Target cupcake div to be deleted 
    let $cupcake = $(e.target).closest('#cupcake-container');
    let cupcakeId = $cupcake.attr('data-id');


    // Pass cupcakeId to axios
     await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
     $cupcake.remove();
  });

  $(listCupcakes);
});
