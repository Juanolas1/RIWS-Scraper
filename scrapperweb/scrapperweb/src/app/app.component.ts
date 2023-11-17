import { Component, OnInit } from '@angular/core';

import { HttpClient,HttpHeaders  } from '@angular/common/http';


interface FilterCondition {
  range?: {
    price?: {
      lte: number;
    };
    score?: {
      lte: number;
    };
    date_release?: {
      gte?: string;
      lte?: string;
    };
  };
  match?: {
    [key: string]: any; 
  };
}

interface SearchQuery {
  from: number;
  size: number;
  query: {
    bool: {
      must: FilterCondition[];
      should?: any[];
      minimum_should_match?: number;
    };
  };
  sort?: any[];  
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'scrapperweb';
  searchTerm: string = '';
  startDateValue!: Date;
  endDateValue!: Date;

    // Nuevas propiedades para sliders
  fechaValue: number = 0; // Valor inicial para el slider de fecha
  precioValue: number = 0; // Valor inicial para el slider de precio
  notaValue: number = 5; // Valor inicial para el slider de nota
  notaMin: number = 0;
  notaMax: number = 10;
  pegi18Checked: boolean = false;
  gogChecked: boolean = false;
  instantGamingChecked: boolean = false;
  sortOrder: string = 'desc';  // 'desc' para Mayor a Menor por defecto


  // Nuevas propiedades para checkboxes de género
  genero1 = { id: 'genero1', label: 'Género 1', checked: false };
  genero2 = { id: 'genero2', label: 'Género 2', checked: false };
  genero3 = { id: 'genero3', label: 'Género 3', checked: false };

  filterOptions = [this.genero1, this.genero2, this.genero3];

  filterRanges = [
    { id: 'fechaSlider', label: 'Fecha', value: this.fechaValue },
    { id: 'precioSlider', label: 'Precio', value: this.precioValue },
    { id: 'notaSlider', label: 'Nota', value: this.notaValue }
  ];

  onSearch() {
    this.pageIndex = 0; // Restablece pageIndex a 0
    this.buscarJuegosPorNombre(this.searchTerm);
    
  }
  


precioMax: number = 200;
precioMin: number = 0;



buscarJuegosPorNombre(nombre?: string) {
  const from = this.pageIndex * this.pageSize;
  const size = this.pageSize;
  const url = `https://localhost:9200/scrapperjuegos-riws-index/_search`;

  
  const conditions: FilterCondition[] = [
    {
      range: {
        "price": {
          "lte": this.precioValue
        }
      }
    },
    {
      range: {
        "score": {
          "lte": this.notaValue
        }
      }
    }
  ];

  // Verifica si alguna de las fechas está definida
  const dateRangeCondition: FilterCondition['range'] = {};
  if (this.startDateValue) {
    const startDate = new Date(this.startDateValue);
    if (!isNaN(startDate.getTime())) {
      dateRangeCondition.date_release = { ...dateRangeCondition.date_release, "gte": startDate.toISOString().split('T')[0] }; // Formato YYYY-MM-DD
    }
  }
  if (this.endDateValue) {
    const endDate = new Date(this.endDateValue);
    if (!isNaN(endDate.getTime())) {
      dateRangeCondition.date_release = { ...dateRangeCondition.date_release, "lte": endDate.toISOString().split('T')[0] }; // Formato YYYY-MM-DD
    }
  }
  if (dateRangeCondition.date_release) {
    conditions.push({ range: dateRangeCondition });
  }
  
  if (this.pegi18Checked) {
    conditions.push({
      match: {
        pegi: "PEGI 18"
      }
    });
  }
  
  if (this.gogChecked) {
    conditions.push({
      match: {
        web: "gog" 
      }
    });
  }

  if (this.instantGamingChecked) {
    conditions.push({
      match: {
        web: "instant-gaming"
      }
    });
  }

  

  let query: SearchQuery;

  // Si hay un nombre, incluye la condición de búsqueda por nombre
  if (nombre && nombre.trim() !== '') {
    query = {
      from,
      size,
      query: {
        bool: {
          must: conditions, // Filtros
          should: [ // Búsqueda por nombre
            {
              match_phrase_prefix: {
                "name": nombre
              }
            },
            {
              match_phrase: {
                "name": nombre
              }
            }
          ],
          minimum_should_match: 1
        }
      }
    };
  } else {
    // Si no hay nombre, busca solo por filtros
    query = {
      from,
      size,
      query: {
        bool: {
          must: conditions
        }
      }
    };
  }


  if (this.sortOrder) {
    query.sort = [
      { "price": { "order": this.sortOrder } }
    ];
  }

  

  const headers = new HttpHeaders({
    'Authorization': 'Basic ' + btoa('elastic:VjcT4+K6O9FWc8lJO=hp'), 
    'Content-Type': 'application/json'
  });

  this.http.post<any>(url, query, { headers }).subscribe(data => {
    this.games = data.hits.hits;
  }, error => {
    console.error('Error en la búsqueda:', error);
  });
}










  showFilterMenu = false;
//  filterOptions = [
//    { id: 'option1', label: 'Opción 1', checked: false },
//  ];
//
//  filterRanges = [
//    { id: 'range1', label: 'Rango 1', value: 0 },
//  ];




  adjustFilterMenuPosition() {
    const navbar = document.querySelector('.navbar') as HTMLElement;
    const filterMenu = document.querySelector('.filter-menu') as HTMLElement;
    if (navbar && filterMenu) {
      const navbarHeight = navbar.getBoundingClientRect().height;
      filterMenu.style.top = `${navbarHeight}px`;
    }
  }

  toggleFilterMenu() {
    this.showFilterMenu = !this.showFilterMenu;
    if (this.showFilterMenu) {
      setTimeout(() => this.adjustFilterMenuPosition(), 0);
    }
  }
  


  games: any[] = []; 

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.precioValue = 200;
    this.buscarJuegosPorNombre(this.searchTerm); 
  }

  pageIndex: number = 0;
  pageSize: number = 20;



scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}
onNextPage() {
  if (this.pageIndex >= 0) {
    this.pageIndex++;
    this.buscarJuegosPorNombre(this.searchTerm);
    this.scrollToTop();
  }
}

onPreviousPage() {
  if (this.pageIndex > 0) {
    this.pageIndex--;
    this.buscarJuegosPorNombre(this.searchTerm);
    this.scrollToTop();
  }
}



onFilterChange() {
  this.buscarJuegosPorNombre(this.searchTerm);
}




}
