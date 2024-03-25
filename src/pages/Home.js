import React, { Component } from 'react'
import ProductList from '../components/ProductList'
import FilterButton from '../components/FilterButton'

export default class Home extends Component {
  render() {
    return (
      <div>
        <FilterButton></FilterButton>
        <ProductList/>
      </div>
    )
  }
}

