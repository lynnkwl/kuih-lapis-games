import Form from 'react-bootstrap/Form';

function TextForm() {
  return (
    <Form>
      <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
        <Form.Label>Change the price</Form.Label>
        <Form.Control type="float" placeholder="15.00" style={{"width":"100px"}}/>
      </Form.Group>
    </Form>
  );
}

export default TextForm;