import React, { Component } from 'react'
import TextForm from '../components/TextForm'
import { Button } from 'react-bootstrap'

export default class Admin extends Component {
  render() {
    return (
      <div>
        <div class='text-center'>
          <TextForm/>
        </div>
        <Button variant="primary">Change price</Button>
      </div>
    )
  }
}
